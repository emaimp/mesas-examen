import axios from 'axios'

// Hook para obtener notas correlativas de un estudiante
export function useCorrelativeNotes () {
  /**
   * Obtiene las notas y el estado de las correlativas para un estudiante
   * @param {number} studentId - El ID del estudiante
   * @returns {Promise<Array>} - Retorna una promesa con un array de notas y correlativas
   */
  const fetchCorrelativeNotes = async studentId => {
    try {
      // Realiza la petición GET para obtener las notas correlativas del estudiante
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/estudiantes/${studentId}/notas_correlativas`)
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error(`Error al obtener notas y correlativas:`, error)
      return []
    }
  }

  return {
    // Expone la función fetchCorrelativeNotes para ser usada en otros componentes
    fetchCorrelativeNotes,
  }
}
