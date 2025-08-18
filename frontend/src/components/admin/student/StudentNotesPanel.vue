<template>
  <div class="notas-panel-wrapper">

    <div v-if="loading" class="text-center py-5">
      <v-progress-circular color="primary" indeterminate />
      <p class="mt-2">Cargando...</p>
    </div>

    <v-alert
      v-else-if="!loading && (!notasData || notasData.length === 0)"
      class="mb-4"
      text="No se encontraron notas para este estudiante."
      type="info"
      variant="tonal"
    />

    <v-expansion-panels v-else multiple variant="accordion">
      <NotasEstudianteTable
        :notas-data="notasData"
      />
    </v-expansion-panels>
  </div>
</template>

<script setup>
  import { useStudentNotas } from '../../../services/student/useStudentNotes'
  import NotasEstudianteTable from '../../admin/student/StudentNotesTable.vue'

  // Define las propiedades que este componente puede recibir
  const props = defineProps({
    studentId: {
      type: [Number, String],
      required: true, // studentId es una propiedad requerida
    },
  })

  // Obtiene la función para buscar notas del estudiante por ID
  const { fetchStudentNotes } = useStudentNotas()

  // Variables reactivas para almacenar los datos de las notas y el estado de carga
  const notasData = ref([]) // Almacena los datos de las notas
  const loading = ref(true) // Indica si los datos están cargando

  // Función para cargar las notas del estudiante
  const loadStudentNotas = async currentStudentId => {
    // Si no hay ID, resetea los datos y el estado de carga
    if (!currentStudentId) {
      notasData.value = []
      loading.value = false
      return
    }

    loading.value = true // Inicia el estado de carga
    try {
      const notas = await fetchStudentNotes(currentStudentId) // Carga las notas
      notasData.value = Array.isArray(notas) ? notas : [] // Asegura que sea un array
    } catch (error) {
      console.error('Error al cargar notas del estudiante:', error)
      notasData.value = [] // En caso de error, resetea los datos
    } finally {
      loading.value = false // Finaliza el estado de carga
    }
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(() => {
    loadStudentNotas(props.studentId) // Carga las notas iniciales del estudiante
  })

  // Observa cambios en la propiedad studentId y recarga las notas
  watch(
    () => props.studentId,
    newStudentId => {
      loadStudentNotas(newStudentId)
    },
  )
</script>

<style scoped>
/* Contenedor principal del panel de notas */
.notas-panel-wrapper {
  height: 100%; /* Ocupa el 100% de la altura disponible */
  display: flex; /* Usa flexbox para el diseño */
  flex-direction: column; /* Organiza los elementos en columna */
}
</style>
