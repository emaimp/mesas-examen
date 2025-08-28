<template>
  <div>
    <div v-if="loading" class="text-center py-5">
      <v-progress-circular color="primary" indeterminate />
      <p class="mt-2 text-white">Cargando...</p>
    </div>

    <v-alert
      v-else-if="
        !loading &&
          (!estudiantesAgrupadosPorAnio || Object.keys(estudiantesAgrupadosPorAnio).length === 0)
      "
      class="mb-4"
      text="No hay estudiantes registrados para esta mesa de examen."
      type="info"
      variant="tonal"
    />

    <v-expansion-panels
      v-else
      v-model="openPanels"
      variant="accordion"
    >
      <v-expansion-panel
        v-for="anioData in sortedEstudiantesAgrupadosPorAnio"
        :key="anioData.anio"
      >
        <v-expansion-panel-title class="text-h6">
          Estudiantes Registrados - {{ getAnioText(anioData.anio) }}
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <div class="transparent-expansion-panel-content">
            <v-row dense>
              <StudentRegisteredCard
                v-for="estudiante in anioData.estudiantes"
                :key="estudiante.id"
                :estudiante="estudiante"
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
          Resgistrar Nota del Estudiante
        </v-card-title>
        <v-card-text v-if="selectedEstudiante">
          <v-list dense>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Estudiante:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedEstudiante.estudiante_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">DNI:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedEstudiante.dni
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Materia:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedEstudiante.materia_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Llamado:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedEstudiante.llamado_inscrito === 'primer_llamado' ? 'Primer Llamado' : 'Segundo Llamado'
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Tipo de Inscripción:</v-list-item-title>
              <v-list-item-subtitle>{{
                formatTipoInscripcion(selectedEstudiante.tipo_inscripcion)
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Fecha y Hora:</v-list-item-title>
              <v-list-item-subtitle>{{
                formatFechaHora(selectedEstudiante.fecha_llamado)
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item class="mb-10">
              <v-list-item-title class="font-weight-bold">Carrera:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedEstudiante.carrera_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-text-field
                v-model="studentGrade"
                label="Nota del Estudiante"
                max="10"
                min="0"
                style="margin-top: 17px;"
                type="number"
                variant="outlined"
              />
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions class="mb-2 mx-2">
          <v-spacer />
          <v-btn
            class="action-button"
            variant="outlined"
            @click="saveGrade"
          >
            Subir Nota
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
  import { useTableExamTeacher } from '../../../services/teacher/useTableExamTeacher'
  import { useAuthUser } from '../../../services/user/useAuthUser'
  import StudentRegisteredCard from '../../teacher/examtables/StudentRegisteredCard.vue'

  // Obtiene el usuario autenticado y la función para cargarlo
  const { user, fetchAuthUser } = useAuthUser()
  // Propiedad computada para obtener el ID del profesor del usuario autenticado
  const teacherId = computed(() => user.value?.id)

  // Obtiene la función para obtener mesas de examen asignadas a un profesor
  const { fetchExamTables } = useTableExamTeacher()

  // Variables reactivas para el estado del componente
  const estudiantesAgrupadosPorAnio = ref([]) // Almacena los estudiantes agrupados por año
  const loading = ref(true) // Indica si los datos están cargando
  const snackbar = ref({
    show: false,
    message: '',
    color: '',
  }) // Estado para mostrar notificaciones al usuario

  const showInscripcionDialog = ref(false) // Controla la visibilidad del diálogo de detalles
  const selectedEstudiante = ref(null) // Almacena el estudiante seleccionado para mostrar detalles
  const openPanels = ref([]) // Controla qué paneles de expansión están abiertos (para agrupar por año)
  const studentGrade = ref(null) // Almacena la nota del estudiante

  // Propiedad computada para ordenar los estudiantes agrupados por año de forma ascendente
  const sortedEstudiantesAgrupadosPorAnio = computed(() => {
    if (!Array.isArray(estudiantesAgrupadosPorAnio.value)) {
      return []
    }
    return [...estudiantesAgrupadosPorAnio.value].sort(
      (a, b) => Number.parseInt(a.anio) - Number.parseInt(b.anio),
    )
  })

  /**
   * Convierte el número del año a un formato ordinal (1° Año, 2° Año, etc.)
   * @param {number} anio - El número del año
   * @returns {string} El texto formateado del año
   */
  const getAnioText = anio => {
    if (typeof anio !== 'number' || anio <= 0 || Number.isNaN(anio)) {
      return 'Año Desconocido'
    }
    return `Año ${anio}`
  }

  /**
   * Formatea una fecha y hora a un string legible.
   * @param {string | Date} fecha - La fecha a formatear.
   * @returns {string} La fecha y hora formateada.
   */
  const formatFechaHora = fecha => {
    if (!fecha) return 'N/A'
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(fecha).toLocaleDateString('es-ES', options)
  }

  /**
   * Abre el diálogo de detalles con el estudiante seleccionado
   * Esta función es llamada por el evento 'open-registered-dialog' de StudentRegisteredCard
   * @param {Object} estudiante - El objeto del estudiante seleccionado
   */
  const openInscripcionDialog = estudiante => {
    selectedEstudiante.value = estudiante
    studentGrade.value = null // Reinicia la nota cuando se abre el diálogo
    showInscripcionDialog.value = true
  }

  const saveGrade = () => {
    // Aquí iría la lógica para guardar la nota, por ejemplo, una llamada a la API
    // Después de guardar, podrías cerrar el diálogo y mostrar un snackbar
    showInscripcionDialog.value = false
    snackbar.value = {
      show: true,
      message: `Nota ${studentGrade.value} guardada para ${selectedEstudiante.value.estudiante_nombre}`,
      color: 'success',
    }
  }

  /**
   * Carga los estudiantes registrados para un profesor específico
   * @param {number|string} currentTeacherId - El ID del profesor
   */
  const loadEstudiantes = async currentTeacherId => {
    if (!currentTeacherId) {
      estudiantesAgrupadosPorAnio.value = []
      loading.value = false
      return
    }
    loading.value = true // Inicia el estado de carga
    try {
      const responseData = await fetchExamTables(currentTeacherId)

      // Filtra los estudiantes para mostrar solo aquellos con estado de inscripción activo
      const activeEstudiantes = responseData.filter(
        estudiante => estudiante.estado === 'active',
      )

      // Agrupa los estudiantes activos por año de la fecha de la mesa
      const groupedEstudiantes = activeEstudiantes.reduce((acc, estudiante) => {
        // Crear una copia del estudiante y ajustar las propiedades para StudentRegisteredCard
        const estudianteParaCard = { ...estudiante }

        // Mapear estudiante_nombre a nombre_estudiante
        estudianteParaCard.nombre_estudiante = estudiante.estudiante_nombre || 'Desconocido'
        // Directamente usar los campos del backend
        estudianteParaCard.llamado_inscrito = estudiante.llamado_inscrito || 'Desconocido'
        estudianteParaCard.fecha_llamado = estudiante.fecha_llamado || null
        // Añadir libreta, dni, carrera_nombre, materia_nombre si no existen
        estudianteParaCard.libreta = estudiante.libreta || 'N/A'
        estudianteParaCard.dni = estudiante.dni || 'N/A'
        estudianteParaCard.carrera_nombre = estudiante.carrera_nombre || 'Desconocida'
        estudianteParaCard.materia_nombre = estudiante.materia_nombre || 'Desconocida'

        const fechaLlamadoParaAgrupar = estudianteParaCard.fecha_llamado ? new Date(estudianteParaCard.fecha_llamado) : null
        const anio = fechaLlamadoParaAgrupar && !Number.isNaN(fechaLlamadoParaAgrupar.getFullYear()) ? fechaLlamadoParaAgrupar.getFullYear() : 'Desconocido'

        if (!acc[anio]) {
          acc[anio] = { anio, estudiantes: [] }
        }
        acc[anio].estudiantes.push(estudianteParaCard) // Usar el objeto modificado
        return acc
      }, {})
      // Convierte el objeto agrupado en un array de valores
      estudiantesAgrupadosPorAnio.value = Object.values(groupedEstudiantes)
    } catch (error) {
      console.error('Error al cargar estudiantes registrados:', error)
      estudiantesAgrupadosPorAnio.value = [] // Resetea los datos en caso de error
    } finally {
      loading.value = false // Finaliza el estado de carga
    }
  }

  // Hook que se ejecuta cuando el componente se monta
  onMounted(async () => {
    // Asegura que el usuario esté cargado si no lo está ya (el layout principal ya lo hace)
    if (!user.value) {
      await fetchAuthUser()
    }
    // La carga de estudiantes se maneja por el watcher con 'immediate: true' (para evitar llamadas duplicadas)
  })

  // Observa cambios en el ID del profesor y recarga los estudiantes si cambia
  watch(teacherId, async (newTeacherId, oldTeacherId) => {
    // Solo recarga si el ID del profesor ha cambiado o si es la carga inicial y no hay datos
    if (newTeacherId && (newTeacherId !== oldTeacherId || estudiantesAgrupadosPorAnio.value.length === 0)) {
      await loadEstudiantes(newTeacherId) // Recarga los estudiantes con el nuevo ID de profesor
      // Abre el primer panel de expansión si hay estudiantes disponibles
      openPanels.value = sortedEstudiantesAgrupadosPorAnio.value.length > 0 ? [0] : []
    }
  }, { immediate: true }) // Ejecuta el watcher inmediatamente al montar el componente

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
.transparent-expansion-panel-content {
  padding: 6px; /* Espaciado interno */
}

/* Estilos para centrar el snackbar de notificaciones */
.centered-snackbar {
  left: 50% !important; /* Centra horizontalmente */
  transform: translateX(-50%) !important; /* Ajuste para centrado perfecto */
  bottom: 0 !important; /* Posiciona en la parte inferior */
  text-align: center; /* Centra el texto dentro del snackbar */
}

/* Estilos para sobreescribir el .v-list global */
.v-list {
  background: linear-gradient(to right, #1f5d8b, #0e4c7a) !important;
}
</style>
