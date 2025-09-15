import axios from 'axios'

// Cache para almacenar resultados de búsquedas
const cache = new Map()
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutos en ms

// Hook para buscar carreras
export function useCareerSearch () {
  /**
   * Función para obtener carreras desde la API con cache
   * @param {string} [query=''] - Parámetro opcional de búsqueda
   * @returns {Promise<Array>} - Retorna una promesa con un array de carreras
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchCareers = async (query = '') => {
    const cacheKey = query || 'all'
    const cached = cache.get(cacheKey)

    // Verificar si hay cache válido
    if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
      return cached.data
    }

    try {
      // Construye la URL de la API, añadiendo el query si existe
      const url = query ? `${import.meta.env.VITE_API_URL}/carreras?query=${encodeURIComponent(query)}` : `${import.meta.env.VITE_API_URL}/carreras`
      // Realiza la petición GET a la API
      const response = await axios.get(url, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Almacenar en cache
      cache.set(cacheKey, {
        data: response.data,
        timestamp: Date.now(),
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
