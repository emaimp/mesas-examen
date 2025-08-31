import axios from 'axios'

// Hook para la inscripción de estudiantes a mesas de examen
export function useTableRegistration () {
  /**
   * Inscribe a un estudiante en una mesa de examen
   * @param {number} estudianteId - El ID del estudiante
   * @param {number} mesaExamenId - El ID de la mesa de examen
   * @param {string} llamadoInscrito - El llamado al que se inscribe ("primer_llamado" o "segundo_llamado")
   * @returns {Promise<object>} - Objeto con el estado de la inscripción (éxito/fallo y mensaje)
   */
  const RegisterStudentToTable = async (estudianteId, mesaExamenId, llamadoInscrito) => {
    // Valida que los IDs sean números válidos y que el llamado sea una cadena
    if (
      typeof estudianteId !== 'number'
      || Number.isNaN(estudianteId)
      || typeof mesaExamenId !== 'number'
      || Number.isNaN(mesaExamenId)
      || typeof llamadoInscrito !== 'string'
      || (llamadoInscrito !== 'primer_llamado'
        && llamadoInscrito !== 'segundo_llamado')
    ) {
      console.error('Error de validación: Los IDs de estudiante y mesa de examen deben ser números válidos y el llamado debe ser "primer_llamado" o "segundo_llamado"')
      return { success: false, message: 'Datos de inscripción inválidos' }
    }

    try {
      // Realiza la petición POST para inscribir al estudiante
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/mesas/inscripciones/`, {
        estudiante_id: estudianteId,
        mesa_examen_id: mesaExamenId,
        llamado_inscrito: llamadoInscrito,
      })

      const responseData = response.data

      // Verifica si la inscripción fue exitosa según la respuesta del backend
      if (responseData.success) {
        return { success: true, message: responseData.message }
      } else {
        // Construye un mensaje de error si la inscripción falla por validación del backend
        const errorMessage = responseData.errors && responseData.errors.length > 0
          ? responseData.errors.join('\n')
          : responseData.message || 'La inscripción falló debido a una validación'

        console.error(`Error de validación del backend:`, errorMessage)
        return { success: false, message: errorMessage }
      }
    } catch (error) {
      // Manejo de errores generales en la petición
      console.error(`Error al inscribir estudiante ${estudianteId} a mesa ${mesaExamenId}:`, error)

      let errorMessage = 'Hubo un problema inesperado en la inscripción'

      if (axios.isAxiosError(error) && error.response) {
        // Error de respuesta del servidor
        const errorResponseData = error.response.data

        if (errorResponseData && errorResponseData.errors && errorResponseData.errors.length > 0) {
          errorMessage = errorResponseData.errors.join('\n')
        } else if (errorResponseData && errorResponseData.message) {
          errorMessage = errorResponseData.message
        } else {
          errorMessage = `Error del servidor: ${error.response.status} - ${error.response.statusText || ''}`
        }
      } else if (error.request) {
        // No se recibió respuesta del servidor
        errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión a internet'
      } else {
        // Error desconocido
        errorMessage = `Error desconocido: ${error.message}`
      }

      return { success: false, message: errorMessage }
    }
  }

  return {
    // Expone la función RegisterStudentToTable para ser usada en otros componentes
    RegisterStudentToTable,
  }
}
