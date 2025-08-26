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
            <v-list-item class="mb-10">
              <v-list-item-title class="font-weight-bold">Carrera:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedEstudiante.carrera_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item style="overflow: visible; padding-top: 10px;">
              <v-text-field
                v-model="studentGrade"
                label="Nota del Estudiante"
                max="10"
                min="0"
                style="margin-top: 10px;"
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
        const anio = new Date(estudiante.fecha).getFullYear()
        if (!acc[anio]) {
          acc[anio] = { anio, estudiantes: [] }
        }
        acc[anio].estudiantes.push(estudiante)
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
</style>
