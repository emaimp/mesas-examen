import axios from 'axios'

// Hook para interactuar con el chatbot Ollama
export function useOllamaChat () {
  // Función auxiliar para obtener el token de autenticación
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token')
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '', // Incluye el token si existe
    }
  }

  /**
   * Envía un mensaje al chatbot Ollama y recibe su respuesta
   * @param {string} message - El mensaje a enviar al chatbot
   * @returns {Promise<string>} - Retorna una promesa con la respuesta del chatbot
   * @throws {Error} - Lanza un error si la comunicación falla
   */
  const sendOllamaMessage = async message => {
    try {
      // Realiza la petición POST al endpoint del chatbot
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/ollama/chat`, {
        message, // El mensaje a enviar en el cuerpo de la petición
      }, {
        headers: getAuthHeaders(), // Usa la función auxiliar para los headers
      })
      // Retorna la respuesta del chatbot
      return response.data.response
    } catch (error) {
      // Inicializa un mensaje de error genérico
      let errorMessage = 'Error inesperado al procesar el mensaje.'
      if (error.response) {
        // Si hay respuesta del servidor, muestra el detalle del error o el mensaje
        errorMessage = error.response.data.detail || 'Error de comunicación.'
      } else if (error.request) {
        // Si la petición fue hecha pero no hubo respuesta, indica un problema de conexión
        errorMessage = 'No se pudo conectar. Verifica tu conexión.'
      } else {
        // Para otros errores (antes de enviar la petición), usa el mensaje de error estándar
        errorMessage = error.message
      }
      console.error('Error en sendOllamaMessage:', error) // console para depuración
      // Lanza un error con el mensaje de error procesado
      throw new Error(errorMessage)
    }
  }

  /**
   * Envía una petición para limpiar el historial de chat del usuario actual
   * @returns {Promise<void>} - Retorna una promesa que se resuelve al limpiar el historial
   * @throws {Error} - Lanza un error si la comunicación falla (excepto 404)
   */
  const clearOllamaChatHistory = async () => {
    try {
      await axios.delete(`${import.meta.env.VITE_API_URL}/ollama/chat/history`, {
        headers: getAuthHeaders(), // Usa la función auxiliar para los headers
      })
    } catch (error) {
      // Si el error es 404 (Not Found), significa que no hay historial para ese usuario
      if (error.response && error.response.status === 404) {
        return // No hacer nada si es 404
      }
      console.error('Error al limpiar el historial del chat:', error) // console para depuración
      const errorMessage = error.response ? error.response.data.detail || 'Error clear history' : 'Error unexpected clear history'
      throw new Error(errorMessage)
    }
  }

  return {
    // Expone las funciones para ser usadas en otros componentes
    sendOllamaMessage,
    clearOllamaChatHistory,
  }
}
