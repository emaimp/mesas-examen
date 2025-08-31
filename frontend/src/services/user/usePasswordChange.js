// Hook para gestionar el cambio de contraseña del usuario
export function usePasswordChange () {
  // Variables reactivas para almacenar el estado de carga, errores y éxito
  const loading = ref(false)
  const error = ref(null)
  const success = ref(false)

  // Función para cambiar la contraseña del usuario
  const changePassword = async (currentPassword, newPassword) => {
    loading.value = true // Indica que la carga ha iniciado
    error.value = null // Limpia cualquier error previo
    success.value = false // Resetea el estado de éxito

    const token = localStorage.getItem('access_token') // Obtiene el token de autenticación del localStorage

    if (!token) {
      error.value = 'No hay token de autenticación disponible.' // Establece un error si no hay token
      loading.value = false // Indica que la carga ha finalizado
      return
    }

    try {
      // Realiza la petición PUT para cambiar la contraseña
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/users/me/password`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json', // Indica que se envía un cuerpo JSON
          'Authorization': `Bearer ${token}`, // Envía el token de autenticación
        },
        body: JSON.stringify({
          current_password: currentPassword, // Contraseña actual
          new_password: newPassword, // Nueva contraseña
        }),
      })

      const data = await response.json() // Parsea la respuesta JSON

      if (!response.ok) {
        throw new Error(data.detail || 'Error al cambiar la contraseña') // Lanza un error si la respuesta no es exitosa
      }

      success.value = true // Establece el estado de éxito
      return data // Retorna los datos de la respuesta
    } catch (error_) {
      // Captura y maneja errores en el cambio de contraseña
      error.value = error_.message // Almacena el mensaje de error
    } finally {
      loading.value = false // Indica que la carga ha finalizado
    }
  }

  return {
    // Expone las variables y la función para ser usadas en el componente
    changePassword,
    loading,
    error,
    success,
  }
}
