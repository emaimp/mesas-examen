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
          :active="appStore.selectedSection === 'management-tables'"
          link
          prepend-icon="mdi-calendar-range"
          title="Gestión de Mesas"
          to="/admin/management-tables"
          value="management-tables"
          @click="appStore.setSelectedSection('management-tables')"
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
          :active="appStore.selectedSection === 'admin-dashboard'"
          link
          prepend-icon="mdi-view-dashboard"
          title="Dashboard"
          to="/admin/dashboard"
          value="admin-dashboard"
          @click="appStore.setSelectedSection('admin-dashboard')"
        />

        <v-list-item
          v-if="user"
          class="upload-active"
          link
          prepend-icon="mdi-upload"
          title="Carga de Archivos"
          value="file-upload"
          @click="openAdminFileUploadDialog"
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
      <AdminFileUpload ref="adminFileUpload" />
    </v-main>

    <ChatBotButton />
  </v-app>
</template>

<script setup>
  import axios from 'axios' // Para realizar peticiones HTTP
  import AdminFileUpload from '@/components/admin/AdminFileUpload.vue'
  import ChatBotButton from '@/components/chatbot/ChatBotButton.vue'
  import { useAppStore } from '@/stores/app' // Store de Pinia para la gestión del estado de la aplicación

  // Estado reactivo para controlar la visibilidad del menú lateral
  const drawer = ref(true)
  const adminFileUpload = ref(null)

  const openAdminFileUploadDialog = () => {
    if (adminFileUpload.value) {
      adminFileUpload.value.openDialog()
    }
  }
  // Inicializa el store de la aplicación
  const appStore = useAppStore()
  // Obtiene los datos del usuario desde el store
  const user = appStore.user
  // Inicializa el enrutador de Vue
  const router = useRouter()

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

/* Estilo para mantener siempre activo el item 'Carga de Archivos' */
.upload-active {
  color: rgba(20, 180, 20, 0.9) !important; /* Color del texto y del icono */
}

/* Estilo para mantener siempre activo el item 'Cerrar Sesión' */
.logout-active {
  color: rgba(255, 0, 0, 0.9) !important; /* Color del texto y del icono */
}
</style>
