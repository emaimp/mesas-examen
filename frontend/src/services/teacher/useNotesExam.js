import axios from 'axios'

// Hook para gestionar notas de examen
export function useExamNotes () {
  // Estado de carga de la petición
  const loading = ref(false)
  // Estado de error de la petición
  const error = ref(null)

  /**
   * Envía la nota de un examen al servidor
   * @param {object} payload - Objeto con los datos de la nota a enviar
   * @returns {Promise<boolean>} - Retorna una promesa que indica si la operación fue exitosa
   */
  const sendExamNote = async payload => {
    loading.value = true
    error.value = null
    try {
      // Construye la URL para calificar el examen
      const url = `${import.meta.env.VITE_API_URL}/notas/examen/calificar/`
      // Realiza la petición POST para enviar la nota
      const response = await axios.post(url, payload)
      // Verifica si la petición fue exitosa
      const isSuccess = (response.status === 200 || response.status === 201) && response.data.success
      if (!isSuccess) {
        // Si no fue exitosa, establece el mensaje de error
        error.value = response.data && response.data.errors && response.data.errors.length > 0
          ? new Error(response.data.errors.join(', '))
          : new Error('Error desconocido al registrar la nota.')
      }
      return isSuccess
    } catch (error_) {
      // Captura y maneja cualquier error en la petición
      error.value = error_
      console.error('Error al enviar la nota del examen:', error_)
      return false
    } finally {
      // Finaliza el estado de carga
      loading.value = false
    }
  }

  return {
    // Expone los estados y la función para ser utilizados en otros componentes
    loading,
    error,
    sendExamNote,
  }
}
