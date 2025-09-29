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
      <router-view v-slot="{ Component, route }">
        <transition mode="out-in" name="fade">
          <keep-alive :max="5">
            <component :is="Component" :key="route.path" />
          </keep-alive>
        </transition>
      </router-view>
    </v-main>

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
  import { useAppStore } from '@/stores/app' // Store de Pinia para la gestión del estado de la aplicación

  // Estado reactivo para controlar la visibilidad del menú lateral
  const drawer = ref(true)
  // Estado reactivo para controlar la visibilidad del indicador de carga
  const isLoading = ref(false)
  // Timeout para delay en mostrar carga
  let loadingTimeout = null
  // Inicializa el store de la aplicación
  const appStore = useAppStore()
  // Obtiene los datos del usuario desde el store
  const user = appStore.user
  // Inicializa el enrutador de Vue
  const router = useRouter()

  // Configura los guards de navegación con delay para mostrar carga
  router.beforeEach((to, from, next) => {
    // Solo mostrar carga si no es navegación interna rápida
    if (to.path !== from.path) {
      loadingTimeout = setTimeout(() => {
        isLoading.value = true
      }, 100)
    }
    next()
  })

  router.afterEach(() => {
    if (loadingTimeout) {
      clearTimeout(loadingTimeout)
      loadingTimeout = null
    }
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
  onMounted(async () => {
    // Verifica si existe un token de acceso
    if (localStorage.getItem('access_token')) {
      await fetchUserData() // Si existe, intenta obtener los datos del usuario
      // Precarga inteligente de rutas críticas admin para acelerar primeras cargas
      if (navigator.connection && navigator.connection.effectiveType !== 'slow-2g' && navigator.connection.effectiveType !== '2g') {
        // Solo en conexiones no lentas
        setTimeout(() => {
          // Precarga de pestañas mediante imports dinámicos
          import('../pages/admin/management-tables.vue').catch(() => {})
          import('../pages/admin/administration-tables.vue').catch(() => {})
          import('../pages/admin/download-acts.vue').catch(() => {})
          import('../pages/admin/administration-dashboard.vue').catch(() => {})
          // Precarga chunks de components internos via dynamic import
          import('../components/admin/DateTimePicker.vue').catch(() => {})
          import('../components/autocomplete/CareerAutocomplete.vue').catch(() => {})
          import('../components/autocomplete/SubjectAutocomplete.vue').catch(() => {})
          import('../components/autocomplete/TeacherAutocomplete.vue').catch(() => {})
        }, 100) // Reducido retardo para acelerar
      }
    } else {
      router.replace('/login') // Si no existe, redirige a la página de login
    }
  })
</script>

<style scoped>
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

/* Transición fade para cambios de pestaña */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
