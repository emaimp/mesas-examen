import axios from 'axios'

// Hook para crear mesas de examen
export function useCrearMesa () {
  /**
   * Función para enviar datos de una nueva mesa de examen a la API
   * @param {object} mesaData - Objeto con los datos de la mesa a crear
   * @returns {Promise<object>} - Retorna una promesa con la respuesta de la API
   * @throws {Error} - Lanza un error si la petición falla
   */
  const createTable = async mesaData => {
    try {
      // Realiza la petición POST a la API para crear una mesa
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/mesas/crear/`, mesaData, {
        headers: {
          'Content-Type': 'application/json', // Indica que el cuerpo de la petición es JSON
        },
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores detallado en caso de fallo en la petición
      console.error('Error al crear mesa de examen:', error)
      if (error.response) {
        // El servidor respondió con un estado de error
        console.error('Respuesta de error del servidor:', error.response.data)
        throw error
      } else if (error.request) {
        // La petición fue hecha pero no se recibió respuesta
        console.error('No se recibió respuesta del servidor:', error.request)
        throw new Error('No se pudo conectar con el servidor. Verifica tu conexión.')
      } else {
        // Error al configurar la petición
        console.error('Error al configurar la petición:', error.message)
        throw new Error('Ocurrió un error inesperado al preparar la creación de la mesa.')
      }
    }
  }

  return {
    // Expone la función createTable para ser usada en otros componentes
    createTable,
  }
}
