import axios from 'axios'

// Hook para buscar carreras
export function useCareerSearch () {
  /**
   * Función para obtener carreras desde la API
   * @param {string} [query=''] - Parámetro opcional de búsqueda
   * @returns {Promise<Array>} - Retorna una promesa con un array de carreras
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchCareers = async (query = '') => {
    try {
      // Construye la URL de la API, añadiendo el query si existe
      const url = query ? `${import.meta.env.VITE_API_URL}/carreras?query=${encodeURIComponent(query)}` : `${import.meta.env.VITE_API_URL}/carreras`
      // Realiza la petición GET a la API
      const response = await axios.get(url, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error('Error al obtener carreras:', error)
      return []
    }
  }

  return {
    // Expone la función fetchCareers para ser usada en otros componentes
    fetchCareers,
  }
}
