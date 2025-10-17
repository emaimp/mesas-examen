import axios from 'axios'

// Hook para gestionar la subida de actas digitales en formato PDF
export function useDigitalActsService () {
  // Variables reactivas para controlar el estado de carga y errores
  const loading = ref(false)
  const error = ref(null)

  /**
   * Sube un archivo PDF de actas digitales al servidor.
   * @param {Blob} pdfBlob - El objeto Blob que contiene el contenido del PDF.
   * @param {string} filename - El nombre del archivo PDF.
   * @returns {Promise<object|null>} - Retorna una promesa con la respuesta del servidor o null en caso de error.
   */
  const uploadDigitalActPdf = async (pdfBlob, filename) => {
    loading.value = true // Indica que la carga ha iniciado
    error.value = null // Limpia cualquier error previo
    try {
      const formData = new FormData() // Crea un nuevo objeto FormData
      formData.append('file', pdfBlob, filename) // Añade el archivo PDF al FormData

      const authToken = sessionStorage.getItem('access_token') // Obtiene el token de autenticación del almacenamiento de sesión

      // Realiza la petición POST para subir el archivo PDF
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/actas/upload_pdf/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data', // Establece el tipo de contenido para la subida de archivos
            'Authorization': `Bearer ${authToken}`, // Incluye el token de autenticación
          },
        },
      )

      // Verifica el estado de la respuesta
      if (response.status === 201) {
        return response.data // Retorna los datos de la respuesta si es exitosa
      } else {
        // Maneja errores si la respuesta no es 201
        error.value = new Error(response.data.detail || 'Error desconocido al subir el PDF.')
        return null
      }
    } catch (error_) {
      error.value = error_ // Captura y almacena el error
      console.error('Error al subir el PDF de actas digitales:', error_) // Muestra el error en consola
      return null
    } finally {
      loading.value = false // Indica que la carga ha finalizado
    }
  }

  return {
    // Expone los estados y la función para ser utilizados en otros componentes
    loading,
    error,
    uploadDigitalActPdf,
  }
}
