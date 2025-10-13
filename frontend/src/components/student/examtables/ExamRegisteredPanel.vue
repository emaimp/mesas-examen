<template>
  <div>
    <div v-if="loading" class="text-center py-5">
      <v-progress-circular color="primary" indeterminate />
      <p class="mt-2 text-white">Cargando...</p>
    </div>

    <v-alert
      v-else-if="
        !loading &&
          (!mesasAgrupadasPorAnio || Object.keys(mesasAgrupadasPorAnio).length === 0)
      "
      class="mb-4"
      text="No hay mesas de examen disponibles para esta carrera."
      type="info"
      variant="tonal"
    />

    <v-expansion-panels
      v-else
      v-model="openPanels"
      variant="accordion"
    >
      <v-expansion-panel
        v-for="anioData in sortedMesasAgrupadasPorAnio"
        :key="anioData.anio"
      >
        <v-expansion-panel-title class="text-h6">
          Mesas de Examen - {{ getAnioText(anioData.anio) }}
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <div class="transparent-expansion-panel">
            <v-row dense>
              <MesaExamenCard
                v-for="mesa in anioData.mesas"
                :key="mesa.id"
                :mesa="mesa"
                @open-registered-dialog="openInscripcionDialog"
              />
            </v-row>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-dialog v-model="showInscripcionDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 text-center mt-2 mx-2">
          Mesa de Examen
        </v-card-title>
        <v-card-text v-if="selectedMesa">
          <v-list dense>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Estudiante:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesa.nombre_estudiante
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">DNI:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesa.dni
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Libreta:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesa.libreta
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Materia:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesa.materia_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Profesor:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesa.profesor_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Llamado:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesa.llamado_inscrito === 'primer_llamado' ? 'Primer Llamado' : 'Segundo Llamado'
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Tipo de Inscripción:</v-list-item-title>
              <v-list-item-subtitle>{{
                formatTipoInscripcion(selectedMesa.tipo_inscripcion)
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Fecha y Hora:</v-list-item-title>
              <v-list-item-subtitle>{{
                formatFechaHora(selectedMesa.fecha_llamado)
              }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions class="mb-2 mx-2">
          <v-spacer />
          <v-btn
            class="action-button"
            :disabled="!selectedMesa || selectedMesa.estado !== 'active' || selectedMesa.asistencia === 'si'"
            variant="outlined"
            @click="confirmInscripcion"
          >
            Cancelar Inscripción
          </v-btn>
          <v-btn
            class="cancel-button"
            variant="text"
            @click="showInscripcionDialog = false"
          >
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="snackbar.show"
      class="centered-snackbar"
      :color="snackbar.color"
      timeout="6000"
    >
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script setup>
  import { useTablesRegistered } from '../../../services/student/useTablesRegistered'
  import { useTablesRegisteredState } from '../../../services/student/useTablesRegisteredState'
  import { useAuthUser } from '../../../services/user/useAuthUser'
  import { useStudentTableStore } from '../../../stores/studentTables'
  import MesaExamenCard from '../../student/examtables/ExamRegisteredCard.vue'

  // Obtiene la función para obtener mesas registradas
  const { fetchTablesRegistered } = useTablesRegistered()
  // Obtiene el usuario autenticado y la función para cargarlo
  const { user, fetchAuthUser } = useAuthUser()
  // Obtiene las funciones del servicio para actualizar el estado de la inscripción
  const { error: updateError, success: updateSuccess, updateRegistrationState } = useTablesRegisteredState()
  // Propiedad computada para obtener el ID del estudiante del usuario autenticado
  const studentId = computed(() => user.value?.id)
  // Store para escuchar cambios de registro entre componentes
  const studentTableStore = useStudentTableStore()

  // Variables reactivas para el estado del componente
  const mesasAgrupadasPorAnio = ref([]) // Almacena las mesas de examen agrupadas por año
  const loading = ref(true) // Indica si los datos de las mesas están cargando
  const snackbar = ref({
    show: false,
    message: '',
    color: '',
  }) // Estado para mostrar notificaciones al usuario

  const showInscripcionDialog = ref(false) // Controla la visibilidad del diálogo de confirmación de baja
  const selectedMesa = ref(null) // Almacena la mesa de examen seleccionada para dar de baja
  const openPanels = ref([]) // Controla qué paneles de expansión están abiertos (para agrupar por año)

  // Propiedad computada para ordenar las mesas agrupadas por año de forma ascendente
  const sortedMesasAgrupadasPorAnio = computed(() => {
    if (!Array.isArray(mesasAgrupadasPorAnio.value)) {
      return []
    }
    return [...mesasAgrupadasPorAnio.value].sort(
      (a, b) => Number.parseInt(a.anio) - Number.parseInt(b.anio),
    )
  })

  /**
   * Formatea una cadena de fecha ISO a un formato legible en español
   * @param {string} isoString - La cadena de fecha en formato ISO
   * @returns {string} La fecha y hora formateada o 'Fecha no disponible'
   */
  const formatFechaHora = isoString => {
    if (!isoString) return 'Fecha no disponible'
    const date = new Date(isoString)
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }
    return date.toLocaleDateString('es-ES', options)
  }

  /**
   * Convierte el número del año a un formato ordinal (1° Año, 2° Año, etc.)
   * @param {number} anio - El número del año
   * @returns {string} El texto formateado del año
   */
  const getAnioText = anio => {
    if (typeof anio !== 'number' || anio <= 0 || Number.isNaN(anio)) {
      return 'Año Desconocido'
    }
    return `${anio}° Año`
  }

  /**
   * Abre el diálogo de confirmación de baja con la mesa de examen seleccionada
   * Esta función es llamada por el evento 'open-registered-dialog' de MesaExamenCard
   * @param {Object} mesa - El objeto de la mesa de examen seleccionada
   */
  const openInscripcionDialog = mesa => {
    selectedMesa.value = mesa
    showInscripcionDialog.value = true
  }

  /**
   * Confirma la baja de la inscripción del estudiante a la mesa seleccionada
   * Aquí se manejaría la lógica para desinscribir al estudiante
   */
  const confirmInscripcion = async () => {
    // Verifica que haya una mesa seleccionada y un ID de estudiante
    if (!selectedMesa.value || !studentId.value) {
      snackbar.value = {
        show: true,
        message: 'Error: Datos para dar de baja incompletos.',
        color: 'error',
      }
      showInscripcionDialog.value = false
      return
    }

    // Lógica para dar de baja la inscripción
    try {
      // Llama a la función para actualizar el estado de la inscripción a 'canceled' (cancelada)
      await updateRegistrationState(selectedMesa.value.id_inscripcion, 'canceled')
      // Si la actualización fue exitosa
      if (updateSuccess.value) {
        // Muestra un mensaje de éxito en el snackbar
        snackbar.value = {
          show: true,
          message: 'Inscripción cancelada con éxito.',
          color: 'success',
        }
        // Recarga las mesas de examen para reflejar el cambio
        await loadMesas(studentId.value)
      } else {
        // Si hubo un error en la actualización, muestra un mensaje de error
        snackbar.value = {
          show: true,
          message: updateError.value || 'Error al cancelar la inscripción.',
          color: 'error',
        }
      }
    } catch (error) {
      // Captura y registra cualquier error inesperado durante el proceso
      console.error('Error en confirmInscripcion:', error)
      // Muestra un mensaje de error inesperado en el snackbar
      snackbar.value = {
        show: true,
        message: 'Error inesperado al cancelar la inscripción.',
        color: 'error',
      }
    } finally {
      // Cierra el diálogo de inscripción
      showInscripcionDialog.value = false
    }
  }

  /**
   * Carga las mesas de examen registradas para un estudiante específico
   * @param {number|string} currentStudentId - El ID del estudiante
   */
  const loadMesas = async currentStudentId => {
    if (!currentStudentId) {
      mesasAgrupadasPorAnio.value = []
      loading.value = false
      return
    }
    loading.value = true // Inicia el estado de carga
    try {
      const responseData = await fetchTablesRegistered(currentStudentId)
      // El backend ya devuelve las mesas agrupadas por año de la materia
      mesasAgrupadasPorAnio.value = Array.isArray(responseData)
        ? responseData
        : []
    } catch (error) {
      console.error('Error al cargar mesas inscriptas:', error)
      mesasAgrupadasPorAnio.value = [] // Resetea los datos en caso de error
    } finally {
      loading.value = false // Finaliza el estado de carga
    }
  }

  // Hook que se ejecuta cuando el componente se monta
  onMounted(async () => {
    await fetchAuthUser() // Carga los datos del usuario autenticado
    await loadMesas(studentId.value) // Carga las mesas registradas usando el ID del estudiante
    // Abre el primer panel de expansión si hay mesas disponibles
    openPanels.value = sortedMesasAgrupadasPorAnio.value.length > 0 ? [0] : []
  })

  // Observa cambios en el ID del estudiante y recarga las mesas si cambia
  watch(studentId, async newStudentId => {
    await loadMesas(newStudentId) // Recarga las mesas con el nuevo ID de estudiante
    // Abre el primer panel de expansión si hay mesas disponibles
    openPanels.value = sortedMesasAgrupadasPorAnio.value.length > 0 ? [0] : []
  })

  // Observa cambios de registro en otras pestañas y recarga datos automáticamente
  watch(
    () => studentTableStore.updateVersion,
    async (newVersion, oldVersion) => {
      if (newVersion > oldVersion && newVersion > 0) {
        await loadMesas(studentId.value)
      }
    },
  )

  /**
   * Formatea el tipo de inscripción para mostrar la primera letra en mayúscula
   * @param {string} tipo - El tipo de inscripción (ej. "libre", "regular")
   * @returns {string} El tipo de inscripción formateado (ej. "Libre", "Regular")
   */
  const formatTipoInscripcion = tipo => {
    if (!tipo) return ''
    return tipo.charAt(0).toUpperCase() + tipo.slice(1)
  }
</script>

<style scoped>
/* Estilos para los paneles de expansión */
.v-expansion-panel {
  background-color: transparent !important; /* Fondo transparente para los paneles */
  margin-bottom: 5px; /* Espacio entre paneles */
}

/* Estilos para el contenido dentro de los paneles de expansión */
.transparent-expansion-panel {
  padding: 25px 0px 0px 0px; /* Relleno interno */
}

/* Estilos para centrar el snackbar de notificaciones */
.centered-snackbar {
  left: 50% !important; /* Centra horizontalmente */
  transform: translateX(-50%) !important; /* Ajuste para centrado perfecto */
  bottom: 0 !important; /* Posiciona en la parte inferior */
  text-align: center; /* Centra el texto dentro del snackbar */
}

/* Estilos para sobreescribir el .v-card */
.v-card {
  background: linear-gradient(to right bottom, #003356, #111c35) !important;
}

/* Estilos para sobreescribir el .v-list global */
.v-list {
  background: linear-gradient(to right bottom, #003356, #111c35) !important;
}
</style>
