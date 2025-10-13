import axios from 'axios'

// Cache para almacenar resultados de búsquedas
const cache = new Map()
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutos en ms

// Hook para buscar profesores
export function useTeacherSearch () {
  /**
   * Obtiene profesores filtrados por carrera y opcionalmente por una consulta de búsqueda con cache
   * @param {number|string} careerId - El ID de la carrera
   * @param {string} [professorQuery=''] - Parámetro opcional de búsqueda para profesores
   * @returns {Promise<Array>} - Retorna una promesa con un array de profesores
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchTeachersByCareer = async (careerId, professorQuery = '') => {
    // Si no hay ID de carrera, retorna un array vacío
    if (!careerId) {
      return []
    }

    const cacheKey = `teachers-${careerId}-${professorQuery || 'all'}`
    const cached = cache.get(cacheKey)

    // Verificar si hay cache válido
    if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
      return cached.data
    }

    try {
      // Construye la URL de la API para buscar profesores por carrera
      const url = `${import.meta.env.VITE_API_URL}/carreras/${careerId}/profesores?query=${encodeURIComponent(professorQuery)}`
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
      // Manejo de errores en la obtención de profesores por carrera
      console.error(`Error al obtener profesores de la carrera ${careerId}:`, error)
      throw error
    }
  }

  /**
   * Obtiene los datos de un profesor por su ID con cache
   * @param {number|string} teacherId - El ID del profesor a buscar
   * @returns {Promise<Object|null>} - Retorna una promesa con los datos del profesor o null si no se encuentra
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchTeacherById = async teacherId => {
    if (!teacherId) {
      return null
    }

    const cacheKey = `teacher-${teacherId}`
    const cached = cache.get(cacheKey)

    // Verificar si hay cache válido
    if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
      return cached.data
    }

    try {
      const url = `${import.meta.env.VITE_API_URL}/profesores/${teacherId}`
      const response = await axios.get(url, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Almacenar en cache
      cache.set(cacheKey, {
        data: response.data,
        timestamp: Date.now(),
      })
      return response.data
    } catch (error) {
      console.error(`Error al obtener datos del profesor con ID ${teacherId}:`, error)
      throw error
    }
  }

  /**
   * Obtiene todos los profesores con filtro opcional por nombre con cache
   * @param {string} [query=''] - Parámetro opcional de búsqueda para profesores
   * @returns {Promise<Array>} - Retorna una promesa con un array de profesores
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchAllTeachers = async (query = '') => {
    const cacheKey = `all-teachers-${query || 'all'}`
    const cached = cache.get(cacheKey)

    // Verificar si hay cache válido
    if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
      return cached.data
    }

    try {
      // Construye la URL de la API para buscar todos los profesores
      const url = `${import.meta.env.VITE_API_URL}/profesores?query=${encodeURIComponent(query)}`
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
      // Manejo de errores en la obtención de todos los profesores
      console.error('Error al obtener todos los profesores:', error)
      throw error
    }
  }

  return {
    // Expone las funciones de búsqueda de profesores
    fetchTeachersByCareer,
    fetchTeacherById,
    fetchAllTeachers,
  }
}
