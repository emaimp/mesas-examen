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
          <div class="transparent-expansion-panel-content">
            <v-row dense>
              <MesaExamenCard
                v-for="mesa in anioData.mesas"
                :key="mesa.id"
                :mesa="mesa"
                @open-inscripcion-dialog="openInscripcionDialog"
              />
            </v-row>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-dialog v-model="showInscripcionDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 text-center">
          Confirmar Inscripción
        </v-card-title>
        <v-card-text v-if="selectedMesa">
          Deseas inscribirte a la siguiente mesa de examen?
          <v-list dense>
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
              <v-list-item-title class="font-weight-bold">Fecha y Hora:</v-list-item-title>
              <v-list-item-subtitle>{{
                formatFechaHora(selectedMesa.fecha)
              }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            class="action-button"
            :disabled="inscripcionLoading[selectedMesa?.id]"
            :loading="inscripcionLoading[selectedMesa?.id]"
            variant="outlined"
            @click="confirmInscripcion"
          >
            Inscribirse
          </v-btn>
          <v-btn
            class="cancel-button"
            variant="text"
            @click="showInscripcionDialog = false"
          >
            Cancelar
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
  import { useTableRegistration } from '../../../services/student/useTableRegistration'
  import { useTablesExam } from '../../../services/student/useTablesExam'
  import { useAuthUser } from '../../../services/user/useAuthUser'
  import MesaExamenCard from '../../student/examtables/ExamTableCard.vue'

  // Inicializa servicios para interactuar con la API
  const { fetchTablesExamByStudentNote } = useTablesExam() // Para obtener mesas de examen
  const { RegisterStudentToTable } = useTableRegistration() // Para registrar estudiantes en mesas
  const { user, fetchAuthUser } = useAuthUser() // Para obtener datos del usuario autenticado

  // Propiedades reactivas para el estado del componente
  const studentId = computed(() => user.value?.id) // ID del estudiante
  const mesasAgrupadasPorAnio = ref([]) // Almacena las mesas de examen agrupadas por año
  const loading = ref(true) // Indica si los datos están cargando.
  const inscripcionLoading = ref({}) // Estado de carga para inscripciones individuales
  const snackbar = ref({ // Controla la visibilidad y contenido de los mensajes de notificación
    show: false,
    message: '',
    color: '',
  })
  const showInscripcionDialog = ref(false) // Controla la visibilidad del diálogo de inscripción
  const selectedMesa = ref(null) // Mesa de examen seleccionada para inscripción
  const openPanels = ref([]) // Controla qué paneles de expansión están abiertos

  // Propiedad computada para ordenar las mesas por año
  const sortedMesasAgrupadasPorAnio = computed(() => {
    if (!Array.isArray(mesasAgrupadasPorAnio.value)) {
      return []
    }
    // Ordena las mesas de examen por año de forma ascendente
    return [...mesasAgrupadasPorAnio.value].sort(
      (a, b) => Number.parseInt(a.anio) - Number.parseInt(b.anio),
    )
  })

  /**
   * Formatea una cadena de fecha ISO a un formato legible en español
   * @param {string} isoString - La cadena de fecha en formato ISO
   * @returns {string} La fecha y hora formateada
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
   * Convierte un número de año a un texto descriptivo (ej. "1° Año")
   * @param {number} anio - El número del año
   * @returns {string} El texto del año
   */
  const getAnioText = anio => {
    if (typeof anio !== 'number' || anio <= 0 || Number.isNaN(anio)) {
      return 'Año Desconocido'
    }
    return `${anio}° Año`
  }

  /**
   * Abre el diálogo de inscripción y establece la mesa seleccionada
   * @param {Object} mesa - El objeto de la mesa de examen a inscribir
   */
  const openInscripcionDialog = mesa => {
    selectedMesa.value = mesa
    showInscripcionDialog.value = true
  }

  /**
   * Confirma la inscripción del estudiante a la mesa de examen seleccionada
   */
  const confirmInscripcion = async () => {
    // Valida que haya una mesa seleccionada y un ID de estudiante
    if (!selectedMesa.value || !studentId.value) {
      snackbar.value = {
        show: true,
        message: 'Error: Datos de inscripción incompletos.',
        color: 'error',
      }
      showInscripcionDialog.value = false
      return
    }

    const mesaId = selectedMesa.value.id
    inscripcionLoading.value = { ...inscripcionLoading.value, [mesaId]: true } // Activa el estado de carga

    try {
      // Llama al servicio para registrar al estudiante
      const result = await RegisterStudentToTable(studentId.value, mesaId)

      // Muestra un mensaje de éxito o error
      snackbar.value = {
        show: true,
        message: result.message,
        color: result.success ? 'success' : 'error',
      }
    } catch (error) {
      console.error('Error inesperado al intentar inscribirse:', error)
      snackbar.value = {
        show: true,
        message: 'Ocurrió un error inesperado en la aplicación.',
        color: 'error',
      }
    } finally {
      inscripcionLoading.value = { ...inscripcionLoading.value, [mesaId]: false } // Desactiva el estado de carga
      showInscripcionDialog.value = false // Cierra el diálogo
    }
  }

  /**
   * Carga las mesas de examen para un estudiante específico
   * @param {number|string} currentStudentId - El ID del estudiante
   */
  const loadMesas = async currentStudentId => {
    if (!currentStudentId) {
      mesasAgrupadasPorAnio.value = []
      loading.value = false
      return
    }
    loading.value = true // Activa el estado de carga
    try {
      // Obtiene las mesas de examen de la API
      const responseData = await fetchTablesExamByStudentNote(currentStudentId)
      mesasAgrupadasPorAnio.value = Array.isArray(responseData)
        ? responseData
        : []
    } catch (error) {
      console.error('Error al cargar mesas de examen:', error)
      mesasAgrupadasPorAnio.value = []
    } finally {
      loading.value = false // Desactiva el estado de carga
    }
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(async () => {
    await fetchAuthUser() // Obtiene los datos del usuario autenticado
    await loadMesas(studentId.value) // Carga las mesas de examen
    // Abre el primer panel si hay mesas disponibles
    openPanels.value = sortedMesasAgrupadasPorAnio.value.length > 0 ? [0] : []
  })

  // Observa cambios en el ID del estudiante y recarga las mesas
  watch(studentId, async newStudentId => {
    await loadMesas(newStudentId)
    // Abre el primer panel si hay mesas disponibles después de la recarga
    openPanels.value = sortedMesasAgrupadasPorAnio.value.length > 0 ? [0] : []
  })
</script>

<style scoped>
/* Estilos para los paneles de expansión */
.v-expansion-panel {
  background-color: transparent !important; /* Fondo transparente */
  margin-bottom: 5px; /* Margen inferior */
}

/* Estilos para el contenido dentro de los paneles de expansión */
.transparent-expansion-panel-content {
  padding: 6px; /* Relleno interno */
}

/* Estilos para la barra de notificación (snackbar) */
.centered-snackbar {
  left: 50% !important; /* Centra horizontalmente */
  transform: translateX(-50%) !important; /* Ajuste para centrado perfecto */
  bottom: 0 !important; /* Alinea en la parte inferior */
  text-align: center; /* Centra el texto */
}
</style>
