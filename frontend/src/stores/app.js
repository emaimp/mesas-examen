import { defineStore } from 'pinia'

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
    selectedSection: null, // Sección actualmente seleccionada en el layout
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
    // Acciones para establecer la sección seleccionada
    setSelectedSection (section) {
      this.selectedSection = section
    },
    // Acciones para limpiar los datos del usuario (cerrar sesión)
    clearUser () {
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
