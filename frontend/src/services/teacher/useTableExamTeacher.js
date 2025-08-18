import axios from 'axios'

// Hook para obtener mesas de examen asignadas a un profesor
export function useTableExamTeacher () {
  // Variables reactivas para almacenar las mesas, el estado de carga y errores
  const examTables = ref([])
  const loading = ref(true)
  const error = ref(null)

  // Función para obtener las mesas de examen desde la API
  const fetchExamTables = async profesor_id => {
    if (!profesor_id) {
      examTables.value = []
      loading.value = false
      return []
    }
    loading.value = true // Indica que la carga ha iniciado
    error.value = null // Limpia cualquier error previo
    try {
      // Asegura que profesor_id sea un número antes de usarlo en la URL
      const numericProfesorId = Number(profesor_id)
      if (Number.isNaN(numericProfesorId)) {
        console.error('Error: profesor_id no es un número válido.', profesor_id)
        examTables.value = []
        loading.value = false
        return []
      }
      // Construye la URL para obtener mesas por ID de profesor
      const url = `${import.meta.env.VITE_API_URL}/mesas/${numericProfesorId}/profesor`
      // Realiza la petición GET a la API
      const response = await axios.get(url)
      examTables.value = response.data || [] // Almacena los datos de las mesas, o un array vacío si no hay datos
      return examTables.value
    } catch (error_) {
      error.value = error_ // Captura y almacena el error
      console.error('Error al obtener mesas de examen para el profesor:', error_) // Muestra el error en consola
      examTables.value = [] // Resetea los datos en caso de error
      return []
    } finally {
      loading.value = false // Indica que la carga ha finalizado
    }
  }

  return {
    // Expone las variables y la función para ser usadas en el componente
    examTables,
    loading,
    error,
    fetchExamTables,
  }
}
