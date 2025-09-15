import axios from 'axios'

// Cache para almacenar resultados de búsquedas
const cache = new Map()
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutos en ms

// Hook para buscar materias
export function useSubjectSearch () {
  /**
   * Obtiene materias filtradas por carrera y opcionalmente por una consulta de búsqueda con cache
   * @param {number|string} careerId - El ID de la carrera
   * @param {string} [subjectQuery=''] - Parámetro opcional de búsqueda para materias
   * @returns {Promise<Array>} - Retorna una promesa con un array de materias
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchSubjectsByCareer = async (careerId, subjectQuery = '') => {
    // Si no hay ID de carrera, retorna un array vacío
    if (!careerId) {
      return []
    }

    const cacheKey = `${careerId}-${subjectQuery || 'all'}`
    const cached = cache.get(cacheKey)

    // Verificar si hay cache válido
    if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
      return cached.data
    }

    try {
      // Construye la URL de la API para buscar materias por carrera
      const url = `${import.meta.env.VITE_API_URL}/carreras/${careerId}/materias?query=${encodeURIComponent(subjectQuery)}`
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
      console.error(`Error al obtener materias de la carrera ${careerId}:`, error)
      throw error
    }
  }

  return {
    // Expone la función fetchSubjectsByCareer para ser usada en otros componentes
    fetchSubjectsByCareer,
  }
}
