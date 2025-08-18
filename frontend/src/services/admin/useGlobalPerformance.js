import axios from 'axios'

// Hook para obtener el rendimiento global de una carrera
export function useRendimientoGlobalCarrera () {
  /**
   * Obtiene el rendimiento global de una carrera específica desde la API
   * @param {number} carreraId - El ID de la carrera
   * @returns {Promise<object|null>} - Retorna una promesa con los datos de rendimiento o null
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchGlobalPerformance = async carreraId => {
    // Verifica si se proporcionó un ID de carrera
    if (!carreraId) {
      console.warn('fetchRendimientoGlobalCarrera: No se proporcionó carreraId')
      return null
    }
    try {
      // Realiza la petición GET para obtener el promedio de notas de la carrera
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/carreras/${carreraId}/notas_promedio`, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error(`Error al obtener el rendimiento global de la carrera ${carreraId}:`, error)
      if (error.response) {
        // El servidor respondió con un estado de error
        console.error('Respuesta de error del servidor:', error.response.data)
        throw new Error(error.response.data.detail || 'Error al obtener el rendimiento global de la carrera')
      } else if (error.request) {
        // La petición fue hecha pero no se recibió respuesta
        console.error('No se recibió respuesta del servidor:', error.request)
        throw new Error('No se pudo conectar con el servidor. Verifica tu conexión')
      } else {
        // Error al configurar la petición
        console.error('Error al configurar la petición:', error.message)
        throw new Error('Ocurrió un error inesperado al preparar la petición')
      }
    }
  }

  return {
    // Expone la función fetchGlobalPerformance para ser usada en otros componentes
    fetchGlobalPerformance,
  }
}
