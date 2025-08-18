import { defineStore } from 'pinia'
import { useOllamaChat } from '@/services/admin/useOllamaChat'

// Definición del store 'app' usando Pinia
export const useAppStore = defineStore('app', {
  // Estado inicial del store
  state: () => ({
    user: {
      id: null, // ID del usuario
      username: null, // Nickname de usuario
      role: null, // Rol del usuario (ej: 'student', 'teacher')
      email: null, // Correo electronico del usuario
      nombre: null, // Nombre completo del usuario
    },
  }),
  // Acciones (metodos) para modificar el estado
  actions: {
    // Acciones para establecer los datos del usuario
    setUser (userData) {
      // Asigna el ID del usuario, o null si no estan presente
      this.user.id = userData.id || null
      // Asigna el nickname del usuario, o null si no estan presente
      this.user.username = userData.username || null
      // Asigna el rol del usuario, o null si no estan presente
      this.user.role = userData.role || null
      // Asigna el correo electronico, o null si no estan presente
      this.user.email = userData.email || null
      // Asigna el nombre del usuario, o null si no estan presente
      this.user.nombre = userData.nombre || null
    },
    // Acciones para limpiar los datos del usuario (cerrar sesión)
    async clearUser () {
      const { clearOllamaChatHistory } = useOllamaChat()
      // Llama a la funcion para limpiar el historial de chat.
      // Los errores ya se manejan dentro de clearOllamaChatHistory.
      await clearOllamaChatHistory()

      this.user.id = null
      this.user.username = null
      this.user.role = null
      this.user.email = null
      this.user.nombre = null
    },
  },
  // Persistencia: Habilita que el estado del store se guarde (ej: en localStorage)
  persist: true,
})
