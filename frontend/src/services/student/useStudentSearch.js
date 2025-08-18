import axios from 'axios'

// Hook para buscar estudiantes
export function useStudentSearch () {
  /**
   * Obtiene estudiantes filtrados por carrera y opcionalmente por una consulta de búsqueda
   * @param {number|string} careerId - El ID de la carrera
   * @param {string} [studentQuery=''] - Parámetro opcional de búsqueda para estudiantes
   * @returns {Promise<Array>} - Retorna una promesa con un array de estudiantes
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchStudentsByCareer = async (careerId, studentQuery = '') => {
    // Si no hay ID de carrera, retorna un array vacío
    if (!careerId) {
      return []
    }
    try {
      // Construye la URL de la API para buscar estudiantes por carrera
      const url = `${import.meta.env.VITE_API_URL}/carreras/${careerId}/estudiantes?query=${encodeURIComponent(studentQuery)}`
      // Realiza la petición GET a la API
      const response = await axios.get(url, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en la obtención de estudiantes por carrera
      console.error(`Error al obtener estudiantes de la carrera ${careerId}:`, error)
      throw error
    }
  }

  /**
   * Obtiene los datos de un estudiante por su ID
   * @param {number|string} studentId - El ID del estudiante a buscar
   * @returns {Promise<Object|null>} - Retorna una promesa con los datos del estudiante o null si no se encuentra
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchStudentById = async studentId => {
    if (!studentId) {
      return null
    }
    try {
      const url = `${import.meta.env.VITE_API_URL}/estudiantes/${studentId}`
      const response = await axios.get(url, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      return response.data
    } catch (error) {
      console.error(`Error al obtener datos del estudiante con ID ${studentId}:`, error)
      throw error
    }
  }

  return {
    // Expone las funciones de búsqueda de estudiantes
    fetchStudentsByCareer,
    fetchStudentById,
  }
}
