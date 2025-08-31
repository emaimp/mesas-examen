import axios from 'axios'

// Hook para subir archivos
export function useFileUpload () {
  // Obtiene los encabezados de autorización, incluyendo el token si existe
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      return {
        'Content-Type': 'multipart/form-data', // Tipo de contenido para subida de archivos
        'Authorization': `Bearer ${token}`, // Token de autenticación
      }
    }
    return {
      'Content-Type': 'multipart/form-data',
    }
  }

  /**
   * Sube un archivo XLSX con datos de usuarios a la API
   * @param {File} file - El archivo a subir
   * @returns {Promise<Object>} - Objeto con el estado de la operación
   */
  const uploadUsersXLSX = async file => {
    if (!file) {
      return { success: false, message: 'No se ha seleccionado ningún archivo de usuarios', errors: null }
    }

    // Crea un objeto FormData para enviar el archivo
    const formData = new FormData()
    formData.append('file', file)

    try {
      // Realiza la petición POST para cargar usuarios
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/usuarios/cargar_excel`, formData, {
        headers: getAuthHeaders(), // Usa los encabezados de autenticación
      })

      // Retorna el resultado de la operación
      return {
        success: response.data.success || false,
        message: response.data.message || 'Respuesta del servidor sin mensaje de usuarios',
        errors: response.data.errors || null,
      }
    } catch (error) {
      // Manejo de errores en la subida de usuarios
      console.error('Error al subir el archivo de usuarios:', error)

      if (error.response) {
        // Error de respuesta del servidor
        console.error('Respuesta de error del servidor de usuarios:', error.response.data)
        console.error('Estado:', error.response.status)
        return {
          success: false,
          message: error.response.data.message || `Error al cargar usuarios (Estado: ${error.response.status})`,
          errors: error.response.data.errors || null,
        }
      } else if (error.request) {
        // No se recibió respuesta del servidor
        console.error('No se recibió respuesta del servidor:', error.request)
        return { success: false, message: 'No se pudo conectar con el servidor de usuarios. Verifica tu conexión', errors: null }
      } else {
        // Error al configurar la petición
        console.error('Error al configurar la petición de usuarios:', error.message)
        return { success: false, message: 'Ocurrió un error inesperado al preparar la subida de usuarios', errors: null }
      }
    }
  }

  /**
   * Sube un archivo XLSX con datos de notas a la API
   * @param {File} file - El archivo a subir
   * @returns {Promise<Object>} - Objeto con el estado de la operación
   */
  const uploadGradesXLSX = async file => {
    if (!file) {
      return { success: false, message: 'No se ha seleccionado ningún archivo de notas', errors: null }
    }

    // Crea un objeto FormData para enviar el archivo
    const formData = new FormData()
    formData.append('file', file)

    try {
      // Realiza la petición POST para cargar notas
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/notas/cargar_excel`, formData, {
        headers: getAuthHeaders(), // Usa los encabezados de autenticación
      })

      // Retorna el resultado de la operación
      return {
        success: response.data.success || false,
        message: response.data.message || 'Respuesta del servidor sin mensaje de notas',
        errors: response.data.errors || null,
      }
    } catch (error) {
      // Manejo de errores en la subida de notas
      console.error('Error al subir el archivo de notas:', error)

      if (error.response) {
        // Error de respuesta del servidor
        console.error('Respuesta de error del servidor:', error.response.data)
        console.error('Estado:', error.response.status)

        return {
          success: false,
          message: error.response.data.message || `Error al cargar notas (Estado: ${error.response.status})`,
          errors: error.response.data.errors || null,
        }
      } else if (error.request) {
        // No se recibió respuesta del servidor
        console.error('No se recibió respuesta del servidor de notas:', error.request)
        return { success: false, message: 'No se pudo conectar con el servidor de notas. Verifica tu conexión', errors: null }
      } else {
        // Error al configurar la petición
        console.error('Error al configurar la petición de notas:', error.message)
        return { success: false, message: 'Ocurrió un error inesperado al preparar la subida de notas', errors: null }
      }
    }
  }

  /**
   * Sube un archivo XLSX con datos de plan_estudios (carreras, materias, materia_carreras y correlativas) a la API
   * @param {File} file - El archivo a subir
   * @returns {Promise<Object>} - Objeto con el estado de la operación
   */
  const uploadPlanEstudiosXLSX = async file => {
    if (!file) {
      return { success: false, message: 'No se ha seleccionado ningún archivo de plan_estudios', errors: null }
    }

    // Crea un objeto FormData para enviar el archivo
    const formData = new FormData()
    formData.append('file', file)

    try {
      // Realiza la petición POST para cargar plan_estudios
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/carreras_materias_correlativas/cargar_excel`, formData, {
        headers: getAuthHeaders(), // Usa los encabezados de autenticación
      })

      // Retorna el resultado de la operación
      return {
        success: response.data.success || false,
        message: response.data.message || 'Respuesta del servidor sin mensaje de plan_estudios',
        errors: response.data.errors || null,
      }
    } catch (error) {
      // Manejo de errores en la subida de plan_estudios
      console.error('Error al subir el archivo de plan_estudios:', error)

      if (error.response) {
        // Error de respuesta del servidor
        console.error('Respuesta de error del servidor:', error.response.data)
        console.error('Estado:', error.response.status)

        return {
          success: false,
          message: error.response.data.message || `Error al cargar plan_estudios (Estado: ${error.response.status})`,
          errors: error.response.data.errors || null,
        }
      } else if (error.request) {
        // No se recibió respuesta del servidor
        console.error('No se recibió respuesta del servidor:', error.request)
        return { success: false, message: 'No se pudo conectar con el servidor de plan_estudios. Verifica tu conexión', errors: null }
      } else {
        // Error al configurar la petición
        console.error('Error al configurar la petición de plan_estudios:', error.message)
        return { success: false, message: 'Ocurrió un error inesperado al preparar la subida de plan_estudios', errors: null }
      }
    }
  }

  return {
    // Expone las funciones para ser usadas en otros componentes
    uploadUsersXLSX,
    uploadGradesXLSX,
    uploadPlanEstudiosXLSX,
  }
}
