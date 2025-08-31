import axios from 'axios'

// Hook para administrar mesas de examen
export function useTablesExamAdmin () {
  /**
   * Obtiene las mesas de examen por carrera
   * @returns {Promise<Array>} Retorna una promesa con un array de mesas de examen
   * @throws {Error} Lanza un error si la petición falla
   */
  const fetchTablesExamByCareer = async () => {
    try {
      // Construye la URL de la API para obtener mesas de examen por carrera
      const url = `${import.meta.env.VITE_API_URL}/mesas/carreras`
      // Realiza la petición GET a la API
      const response = await axios.get(url, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error('Error al obtener mesas de examen por carrera:', error)
      return []
    }
  }

  /**
   * Elimina una mesa de examen por su ID
   * @param {number} mesaExamenId - El ID de la mesa de examen a eliminar
   * @returns {Promise<object>} Retorna una promesa con el resultado de la eliminación
   * @throws {Error} Lanza un error si la petición falla
   */
  const deleteTableExam = async mesaExamenId => {
    try {
      // Construye la URL de la API para eliminar una mesa de examen
      const url = `${import.meta.env.VITE_API_URL}/mesas/${mesaExamenId}`
      // Realiza la petición DELETE a la API
      const response = await axios.delete(url, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error(`Error al eliminar mesa de examen con ID ${mesaExamenId}:`, error)
      if (error.response) {
        throw new Error(error.response.data.detail || 'Error al eliminar la mesa de examen')
      } else if (error.request) {
        throw new Error('No se pudo conectar con el servidor. Verifica tu conexión')
      } else {
        throw new Error('Ocurrió un error inesperado al preparar la eliminación de la mesa')
      }
    }
  }

  return {
    // Expone las funciones para ser usadas en otros componentes
    fetchTablesExamByCareer,
    deleteTableExam,
  }
}
