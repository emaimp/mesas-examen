import axios from 'axios'

// Hook para obtener mesas de examen
export function useTablesExam () {
  /**
   * Obtiene las mesas de examen filtradas por la nota del estudiante
   * @param {number} estudianteId - El ID del estudiante
   * @returns {Promise<Array>} - Retorna una promesa con un array de mesas de examen
   */
  const fetchTablesExamByStudentNote = async estudianteId => {
    // Si no hay ID de estudiante, advierte y retorna un array vacío
    if (!estudianteId) {
      console.warn('fetchTablesExamByStudentNote: No se proporcionó estudianteId')
      return []
    }
    try {
      // Realiza la petición GET para obtener mesas de examen por nota del estudiante
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/mesas/${estudianteId}/nota`)
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en la obtención de mesas de examen
      console.error(`Error al obtener mesas de examen para estudiante ${estudianteId}:`, error)
      return []
    }
  }

  return {
    // Expone la función fetchTablesExamByStudentNote para ser usada en otros componentes
    fetchTablesExamByStudentNote,
  }
}
