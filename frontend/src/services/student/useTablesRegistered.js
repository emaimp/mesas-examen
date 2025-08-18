import axios from 'axios'

// Hook para obtener mesas de examen en las que un estudiante está inscrito
export function useTablesRegistered () {
  /**
   * Obtiene las mesas de examen en las que un estudiante está inscrito
   * @param {number} estudianteId - El ID del estudiante
   * @returns {Promise<Array>} - Retorna una promesa con un array de mesas inscritas
   * @throws {Error} - Lanza un error si la petición falla
   */
  const fetchTablesRegistered = async estudianteId => {
    // Si no hay ID de estudiante, advierte y retorna un array vacío
    if (!estudianteId) {
      console.warn('fetchTablesRegistered: No se proporcionó estudianteId')
      return []
    }
    try {
      // Realiza la petición GET para obtener las mesas inscritas del estudiante
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/estudiantes/${estudianteId}/mesas_inscriptas`, {
        headers: { Accept: 'application/json' },
        responseType: 'json',
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en la obtención de mesas inscritas
      console.error(`Error al obtener mesas inscriptas para el estudiante ${estudianteId}:`, error)
      return []
    }
  }

  return {
    // Expone la función fetchTablesRegistered para ser usada en otros componentes
    fetchTablesRegistered,
  }
}
