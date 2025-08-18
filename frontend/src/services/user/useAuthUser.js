import axios from 'axios'

// Hook para gestionar la autenticación del usuario
export function useAuthUser () {
  // Variables reactivas para almacenar el usuario, el estado de carga y errores
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Función para obtener los datos del usuario autenticado
  const fetchAuthUser = async () => {
    loading.value = true // Indica que la carga ha iniciado
    error.value = null // Limpia cualquier error previo
    try {
      // Realiza la petición GET para obtener los datos del usuario actual
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/auth/users/me/`, {
        headers: {
          Accept: 'application/json', // Indica que se espera una respuesta JSON
          Authorization: `Bearer ${localStorage.getItem('access_token')}`, // Envía el token de autenticación
        },
      })
      user.value = response.data // Almacena los datos del usuario
    } catch (error_) {
      // Captura y maneja errores en la obtención de datos del usuario
      console.error('Error al obtener datos del usuario autenticado:', error_)
      error.value = error_ // Almacena el error
      user.value = null // Resetea el usuario a null en caso de error
    } finally {
      loading.value = false // Indica que la carga ha finalizado
    }
  }

  return {
    // Expone las variables y la función para ser usadas en el componente
    user,
    loading,
    error,
    fetchAuthUser,
  }
}
