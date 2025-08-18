<template>
  <div class="notas-panel-wrapper">
    <div v-if="loading" class="text-center py-5">
      <v-progress-circular color="primary" indeterminate />
      <p class="mt-2">Cargando información..</p>
    </div>

    <v-alert
      v-else-if="!loading && (!aniosData || aniosData.length === 0)"
      class="mb-4"
      text="No se encontraron notas ni correlativas para este estudiante."
      type="info"
      variant="tonal"
    />

    <v-expansion-panels
      v-else
      v-model="openPanel"
      variant="accordion"
    >
      <NotasCorrelativasTable
        v-for="anio in aniosData"
        :key="anio.anio"
        :anio-data="anio"
      />
    </v-expansion-panels>
  </div>
</template>

<script setup>
  import { useCorrelativeNotes } from '../../../services/student/useCorrelativeNotes'
  import { useAuthUser } from '../../../services/user/useAuthUser'
  import NotasCorrelativasTable from './CorrelativeNotesTable.vue'

  // Desestructura propiedades del servicio de autenticación de usuario
  const { user, loading: _authLoading, error: _authError, fetchAuthUser } = useAuthUser()

  // Propiedades reactivas para el estado del componente
  const loading = ref(true) // Indica si los datos están cargando
  const aniosData = ref([]) // Almacena los datos de notas agrupados por año
  const openPanel = ref(0) // Controla qué panel de expansión está abierto

  // Inicializa el servicio para obtener notas correlativas
  const { fetchCorrelativeNotes } = useCorrelativeNotes()

  /**
   * Carga las notas correlativas para un estudiante específico
   * @param {number|string} currentStudentId - El ID del estudiante
   */
  const loadNotasCorrelativas = async currentStudentId => {
    // Si no hay ID de estudiante, limpia los datos y desactiva la carga
    if (!currentStudentId) {
      aniosData.value = []
      loading.value = false
      return
    }

    loading.value = true // Activa el estado de carga
    try {
      // Obtiene las notas correlativas de la API
      const notas = await fetchCorrelativeNotes(currentStudentId)
      // Asigna los datos obtenidos, asegurándose de que sea un array
      aniosData.value = Array.isArray(notas) ? notas : []
      // Abre el primer panel si hay datos, de lo contrario, no abre ninguno
      openPanel.value = aniosData.value.length > 0 ? 0 : undefined
    } catch (error) {
      console.error('Error al cargar notas y correlativas:', error)
      aniosData.value = [] // En caso de error, limpia los datos
    } finally {
      loading.value = false // Desactiva el estado de carga
    }
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(async () => {
    await fetchAuthUser() // Obtiene los datos del usuario autenticado
    // Si el usuario y su ID existen, carga las notas correlativas
    if (user.value && user.value.id) {
      loadNotasCorrelativas(user.value.id)
    } else {
      loading.value = false // Si no hay usuario, desactiva la carga
    }
  })

  // Observa cambios en el ID del usuario y recarga las notas correlativas
  watch(
    () => user.value?.id,
    newStudentId => {
      loadNotasCorrelativas(newStudentId)
    },
  )
</script>

<style scoped>
/* Estilos para el contenedor principal del panel de notas */
.notas-panel-wrapper {
  display: flex; /* Usa flexbox para el diseño */
  justify-content: center; /* Centra los elementos horizontalmente */
  align-items: center; /* Centra los elementos verticalmente */
  flex-direction: column; /* Organiza los elementos en una columna */
}
</style>
