import axios from 'axios'

// Hook para gestionar el estado de las inscripciones a mesas de examen
export function useTablesRegisteredState () {
  // Estados reactivos para manejar la carga, errores y éxito de la operación
  const loading = ref(false)
  const error = ref(null)
  const success = ref(false)

  /**
   * Actualiza el estado de una inscripción a mesa de examen.
   * @param {number} inscripcionId - El ID de la inscripción a actualizar.
   * @param {string} newState - El nuevo estado para la inscripción.
   */
  const updateRegistrationState = async (inscripcionId, newState) => {
    loading.value = true // Indica que la operación está en curso
    error.value = null // Reinicia el estado de error
    success.value = false // Reinicia el estado de éxito
    try {
      // Realiza una petición PATCH para actualizar el estado de la inscripción
      const response = await axios.patch(`/api/mesas/inscripciones/${inscripcionId}/estado`, {
        estado: newState, // Envía el nuevo estado en el cuerpo de la petición
      })
      // Verifica si la actualización fue exitosa según la respuesta del servidor
      if (response.data.success) {
        success.value = true // Marca la operación como exitosa
        console.log(response.data.message) // Muestra el mensaje de éxito en consola
      } else {
        // Si hay errores, los almacena o muestra un mensaje genérico
        error.value = response.data.errors ? response.data.errors.join(', ') : 'Error desconocido al actualizar el estado.'
      }
    } catch (error_) {
      // Captura y maneja errores de red o del servidor
      error.value = error_.response?.data?.detail || 'Error de red o del servidor.'
      console.error('Error al actualizar el estado de la inscripción:', error_)
    } finally {
      loading.value = false // Finaliza la carga, independientemente del resultado
    }
  }

  return {
    // Expone los estados y la función para ser utilizados en otros componentes
    loading,
    error,
    success,
    updateRegistrationState,
  }
}
