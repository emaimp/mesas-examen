import axios from 'axios'

// Hook para obtener detalles de inscripciones a examen para un profesor
export function useDetailExam () {
  // Variables reactivas para almacenar los detalles, el estado de carga y errores
  const detailExams = ref([])
  const loading = ref(true)
  const error = ref(null)

  /**
   * Función para obtener los detalles de las inscripciones a examen desde la API
   * @param {number|string} profesor_id - El ID del profesor
   * @returns {Promise<Array>} - Retorna una promesa con un array de detalles de examen
   */
  const fetchDetailExams = async profesor_id => {
    if (!profesor_id) {
      detailExams.value = []
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
        detailExams.value = []
        loading.value = false
        return []
      }
      // Construye la URL para obtener los detalles de examen por ID de profesor
      const url = `${import.meta.env.VITE_API_URL}/mesas/${numericProfesorId}/detalle/examen`
      // Realiza la petición GET a la API
      const response = await axios.get(url)
      detailExams.value = response.data || [] // Almacena los datos
      return detailExams.value
    } catch (error_) {
      error.value = error_ // Captura y almacena el error
      console.error('Error al obtener detalles de examen para el profesor:', error_) // Muestra el error en consola
      detailExams.value = [] // Resetea los datos en caso de error
      return []
    } finally {
      loading.value = false // Indica que la carga ha finalizado
    }
  }

  return {
    // Expone los estados y la función para ser utilizados en otros componentes
    detailExams,
    loading,
    error,
    fetchDetailExams,
  }
}
