import axios from 'axios'

// Hook para obtener notas de un estudiante
export function useStudentNotas () {
  /**
   * Obtiene las notas de un estudiante específico desde la API
   * @param {number} studentId - El ID del estudiante
   * @returns {Promise<object>} - Retorna una promesa con los datos de las notas
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchStudentNotes = async studentId => {
    try {
      // Realiza la petición GET para obtener las notas del estudiante
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/notas/${studentId}`)
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error('Error al obtener notas del estudiante:', error)
      throw error
    }
  }

  return {
    // Expone la función fetchStudentNotes para ser usada en otros componentes
    fetchStudentNotes,
  }
}
