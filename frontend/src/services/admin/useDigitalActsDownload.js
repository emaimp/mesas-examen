import axios from 'axios'

// Hook para descargar actas digitales
export function useDigitalActsDownload () {
  // Función auxiliar para obtener el token de autenticación
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token')
    return {
      Accept: 'application/pdf', // Esperamos un PDF como respuesta
      Authorization: token ? `Bearer ${token}` : '', // Incluye el token si existe
    }
  }

  /**
   * Descarga un acta digital en formato PDF por su ID.
   * @param {number} pdfId - El ID del PDF a descargar.
   * @param {string} filename - El nombre del archivo para guardar el PDF.
   * @returns {Promise<void>} - Retorna una promesa que se resuelve al completar la descarga.
   * @throws {Error} - Lanza un error si la petición falla.
   */
  const downloadPdfById = async (pdfId, filename) => {
    if (!pdfId) {
      console.error('downloadPdfById: No se proporcionó un ID de PDF.')
      throw new Error('No se proporcionó un ID de PDF para descargar.')
    }
    if (!filename) {
      console.warn('downloadPdfById: No se proporcionó un nombre de archivo, se usará un nombre genérico.')
      filename = `acta_digital_${pdfId}.pdf`
    }

    try {
      // Construye la URL de la API para descargar el PDF
      const url = `${import.meta.env.VITE_API_URL}/actas/download_pdf/${pdfId}`
      // Realiza la petición GET a la API, esperando un blob (archivo binario)
      const response = await axios.get(url, {
        headers: getAuthHeaders(), // Usa los encabezados de autenticación
        responseType: 'blob', // Importante para manejar la descarga de archivos
      })

      // Crea un objeto URL para el blob y un enlace para la descarga
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = filename // Establece el nombre del archivo para la descarga
      document.body.append(link) // Usar append en lugar de appendChild
      link.click() // Simula un clic para iniciar la descarga
      link.remove() // Usar remove en lugar de removeChild
      window.URL.revokeObjectURL(link.href) // Libera el objeto URL
    } catch (error) {
      // Manejo de errores en caso de fallo en la petición
      console.error(`Error al descargar el PDF con ID '${pdfId}':`, error)
      if (error.response) {
        // Si el servidor devuelve un error, intenta leer el mensaje de error del blob
        const errorBlob = new Blob([error.response.data], { type: 'application/json' })
        const errorText = await errorBlob.text() // Usar Blob#text()
        try {
          const errorData = JSON.parse(errorText)
          throw new Error(errorData.detail || `Error al descargar PDF (Estado: ${error.response.status}).`)
        } catch { // Eliminar catch binding no utilizado
          throw new Error(`Error al descargar PDF (Estado: ${error.response.status}). No se pudo leer el mensaje de error.`)
        }
      } else if (error.request) {
        // La petición fue hecha pero no se recibió respuesta
        throw new Error('No se pudo conectar con el servidor. Verifica tu conexión.')
      } else {
        // Error al configurar la petición
        throw new Error('Ocurrió un error inesperado al preparar la descarga del PDF.')
      }
    }
  }

  return {
    // Expone la función downloadPdfById para ser usada en otros componentes
    downloadPdfById,
  }
}
