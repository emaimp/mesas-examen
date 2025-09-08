import axios from 'axios'

// Hook para obtener actas digitales por nombre de usuario
export function useDigitalActsUploader () {
  // Función auxiliar para obtener el token de autenticación
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token')
    return {
      Accept: 'application/json',
      Authorization: token ? `Bearer ${token}` : '', // Incluye el token si existe
    }
  }

  /**
   * Obtiene una lista de actas digitales subidas por un usuario, filtradas por su nombre.
   * @param {string} nombre - El nombre del usuario que subió el PDF.
   * @returns {Promise<Array>} - Retorna una promesa con un array de actas digitales.
   * @throws {Error} - Lanza un error si la petición falla.
   */
  const fetchPdfsByUploaderName = async nombre => {
    if (!nombre) {
      console.warn('fetchPdfsByUploaderName: No se proporcionó un nombre de usuario.')
      return []
    }
    try {
      // Construye la URL de la API, añadiendo el nombre como parámetro de consulta
      const url = `${import.meta.env.VITE_API_URL}/actas/pdfs_por_uploader/?nombre=${encodeURIComponent(nombre)}`
      // Realiza la petición GET a la API
      const response = await axios.get(url, {
        headers: getAuthHeaders(), // Usa los encabezados de autenticación
        responseType: 'json',
      })
      // Retorna los datos de la respuesta
      return response.data
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error(`Error al obtener PDFs subidos por el usuario '${nombre}':`, error)
      if (error.response) {
        // El servidor respondió con un estado de error
        console.error('Respuesta de error del servidor:', error.response.data)
        throw new Error(error.response.data.detail || 'Error al obtener PDFs por nombre de usuario.')
      } else if (error.request) {
        // La petición fue hecha pero no se recibió respuesta
        console.error('No se recibió respuesta del servidor:', error.request)
        throw new Error('No se pudo conectar con el servidor. Verifica tu conexión.')
      } else {
        // Error al configurar la petición
        console.error('Error al configurar la petición:', error.message)
        throw new Error('Ocurrió un error inesperado al preparar la petición.')
      }
    }
  }

  return {
    // Expone la función fetchPdfsByUploaderName para ser usada en otros componentes
    fetchPdfsByUploaderName,
  }
}
