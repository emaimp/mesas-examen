<template>
  <v-app class="gradient-background">
    <v-navigation-drawer
      v-model="drawer"
      app
      expand-on-hover
      rail
    >
      <v-list>
        <v-list-item
          v-if="user"
          prepend-icon="mdi-account-circle"
          :subtitle="user.email"
          :title="user.username"
        />
      </v-list>

      <v-divider />

      <v-list density="compact" nav>
        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'admin-home'"
          link
          prepend-icon="mdi-home"
          title="Inicio"
          to="/admin"
          value="admin-home"
          @click="appStore.setSelectedSection('admin-home')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'administration-chatbot'"
          link
          prepend-icon="mdi-robot"
          title="Chat Bot"
          to="/admin/administration-chatbot"
          value="administration-chatbot"
          @click="appStore.setSelectedSection('administration-chatbot')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'management-tables'"
          link
          prepend-icon="mdi-calendar-check"
          title="Creación de Mesas"
          to="/admin/management-tables"
          value="management-tables"
          @click="appStore.setSelectedSection('management-tables')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'administration-tables'"
          link
          prepend-icon="mdi-calendar-remove"
          title="Gestión de Mesas"
          to="/admin/administration-tables"
          value="administration-tables"
          @click="appStore.setSelectedSection('administration-tables')"
        />

        <v-list-item
          v-if="false"
          :active="appStore.selectedSection === 'management-teacher'"
          link
          prepend-icon="mdi-account-tie"
          title="Gestión de Profesores"
          to="/admin/management-teacher"
          value="management-teacher"
          @click="appStore.setSelectedSection('management-teacher')"
        />

        <v-list-item
          v-if="false"
          :active="appStore.selectedSection === 'management-student'"
          link
          prepend-icon="mdi-account-school"
          title="Gestión de Estudiantes"
          to="/admin/management-student"
          value="management-student"
          @click="appStore.setSelectedSection('management-student')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'download-acts'"
          link
          prepend-icon="mdi-archive-arrow-down"
          title="Descargar Actas"
          to="/admin/download-acts"
          value="download-acts"
          @click="appStore.setSelectedSection('download-acts')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'administration-dashboard'"
          link
          prepend-icon="mdi-view-dashboard"
          title="Dashboard"
          to="/admin/administration-dashboard"
          value="administration-dashboard"
          @click="appStore.setSelectedSection('administration-dashboard')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'change-password'"
          class="change-active"
          link
          prepend-icon="mdi-key-variant"
          title="Cambiar Contraseña"
          to="/admin/change-password"
          value="change-password"
          @click="appStore.setSelectedSection('change-password')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'administration-upload'"
          class="upload-active"
          link
          prepend-icon="mdi-upload"
          title="Carga de Archivos"
          to="/admin/administration-upload"
          value="administration-upload"
          @click="appStore.setSelectedSection('administration-upload')"
        />

        <v-list-item
          class="logout-active"
          link
          prepend-icon="mdi-logout"
          title="Cerrar Sesión"
          value="logout"
          variant="tonal"
          @click="logout"
        />
      </v-list>
    </v-navigation-drawer>

    <v-main class="d-flex align-center justify-center">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </v-main>
    <ChatBotButton v-if="route.path !== '/admin/administration-chatbot'" />

    <v-overlay
      class="align-center justify-center"
      contained
      :model-value="isLoading"
      persistent
    >
      <v-progress-circular
        color="primary"
        indeterminate
        size="60"
      />
    </v-overlay>
  </v-app>
</template>

<script setup>
  import axios from 'axios' // Para realizar peticiones HTTP
  import { useRoute } from 'vue-router' // Importa useRoute para acceder a la ruta actual
  import ChatBotButton from '@/components/chatbot/ChatBotButton.vue'
  import { useAppStore } from '@/stores/app' // Store de Pinia para la gestión del estado de la aplicación

  // Estado reactivo para controlar la visibilidad del menú lateral
  const drawer = ref(true)
  // Estado reactivo para controlar la visibilidad del indicador de carga
  const isLoading = ref(false)
  // Inicializa el store de la aplicación
  const appStore = useAppStore()
  // Obtiene los datos del usuario desde el store
  const user = appStore.user
  // Inicializa el enrutador de Vue
  const router = useRouter()
  // Obtiene la ruta actual
  const route = useRoute()

  // Configura los guards de navegación para mostrar/ocultar el indicador de carga
  router.beforeEach((to, from, next) => {
    isLoading.value = true
    next()
  })

  router.afterEach(() => {
    isLoading.value = false
  })

  /**
   * Función para cerrar la sesión del usuario
   * Limpia los datos del usuario en el store, elimina el token de acceso y redirige a la página de login
   */
  const logout = () => {
    appStore.clearUser() // Limpia los datos del usuario en el store
    localStorage.removeItem('access_token') // Elimina el token de acceso del almacenamiento local
    nextTick(() => {
      router.replace('/login') // Redirige a la página de login
    })
  }

  /**
   * Función para obtener los datos del usuario autenticado desde la API
   */
  const fetchUserData = async () => {
    try {
      // Realiza una petición GET para obtener los datos del usuario actual
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/auth/users/me/`, {
        headers: {
          Accept: 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`, // Incluye el token de autenticación
        },
      })
      appStore.setUser(response.data) // Establece los datos del usuario en el store
    } catch (error) {
      console.error('Error fetching user data in admin layout:', error)
      appStore.clearUser() // Limpia los datos del usuario en caso de error
      localStorage.removeItem('access_token') // Elimina el token de acceso
      nextTick(() => {
        router.replace('/login') // Redirige a la página de login
      })
    }
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(() => {
    // Verifica si existe un token de acceso
    if (localStorage.getItem('access_token')) {
      fetchUserData() // Si existe, intenta obtener los datos del usuario
    } else {
      router.replace('/login') // Si no existe, redirige a la página de login
    }
  })
</script>

<style scoped>
/* Estilos para el cajón de navegación (menú lateral) */
.v-navigation-drawer {
  z-index: 9999 !important; /* Asegura que el menú esté por encima de otros elementos */
}

/* Estilo para mantener siempre activo el item 'Cambiar Contraseña' */
.change-active {
  color: rgba(250, 210, 1, 0.9) !important; /* Color del texto y del icono */
}

/* Estilo para mantener siempre activo el item 'Carga de Archivos' */
.upload-active {
  color: rgba(20, 180, 20, 0.9) !important; /* Color del texto y del icono */
}

/* Estilo para mantener siempre activo el item 'Cerrar Sesión' */
.logout-active {
  color: rgba(255, 0, 0, 0.9) !important; /* Color del texto y del icono */
}
</style>
