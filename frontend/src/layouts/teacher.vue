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
          prepend-icon="mdi-account-circle"
          :title="user ? user.nombre : ''"
        >
          <v-list-item-subtitle class="email-subtitle">{{ user ? user.email : '' }}</v-list-item-subtitle>
        </v-list-item>
      </v-list>

      <v-divider />

      <v-list density="compact" nav>
        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'teacher-profile'"
          link
          prepend-icon="mdi-account-details"
          title="Perfil"
          :to="user ? `/teacher/${encodeURIComponent(user.nombre)}/profile` : ''"
          value="teacher-profile"
          @click="appStore.setSelectedSection('teacher-profile')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'tables-assigned'"
          link
          prepend-icon="mdi-calendar-check"
          title="Mesas Examen Asignadas"
          :to="user ? `/teacher/${encodeURIComponent(user.nombre)}/tables-assigned` : ''"
          value="tables-assigned"
          @click="appStore.setSelectedSection('tables-assigned')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'digital-acts'"
          link
          prepend-icon="mdi-archive"
          title="Actas Digitales"
          :to="user ? `/teacher/${encodeURIComponent(user.nombre)}/digital-acts` : ''"
          value="digital-acts"
          @click="appStore.setSelectedSection('digital-acts')"
        />

        <v-list-item
          v-if="user"
          :active="appStore.selectedSection === 'change-password'"
          class="change-active"
          link
          prepend-icon="mdi-key-variant"
          title="Cambiar Contraseña"
          :to="user ? `/teacher/${encodeURIComponent(user.nombre)}/change-password` : ''"
          value="change-password"
          @click="appStore.setSelectedSection('change-password')"
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
          <keep-alive :max="1">
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
  import { useAuthUser } from '@/services/user/useAuthUser'
  import { useAppStore } from '@/stores/app' // Store de Pinia para la gestión del estado de la aplicación

  // Estado reactivo para controlar la visibilidad del menú lateral
  const drawer = ref(true)
  // Estado reactivo para controlar la visibilidad del indicador de carga
  const isLoading = ref(false)
  // Timeout para delay en mostrar carga
  let loadingTimeout = null
  // Inicializa el store de la aplicación
  const appStore = useAppStore()
  // Inicializa el enrutador de Vue
  const router = useRouter()
  // Desestructura propiedades del servicio de autenticación de usuario
  const { user, fetchAuthUser } = useAuthUser()

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

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(async () => {
    // Verifica si existe un token de acceso
    if (localStorage.getItem('access_token')) {
      await fetchAuthUser() // Si existe, intenta obtener los datos del usuario
      // Precarga inteligente de rutas críticas teacher para acelerar primeras cargas
      if (navigator.connection && navigator.connection.effectiveType !== 'slow-2g' && navigator.connection.effectiveType !== '2g') {
        // Solo en conexiones no lentas
        setTimeout(() => {
          // Precarga de pestañas mediante imports dinámicos
          import('../pages/teacher/[name]/tables-assigned.vue').catch(() => {})
          import('../pages/teacher/[name]/digital-acts.vue').catch(() => {})
        }, 100) // Reducido retardo para acelerar
      }
    } else {
      router.replace('/login') // Si no existe, redirige a la página de login
    }
  })
</script>

<style scoped>
/* Estilos para el subtítulo del email en el menú */
.email-subtitle {
  font-size: 0.70rem; /* Tamaño de fuente reducido */
  white-space: nowrap; /* Evita el salto de línea */
  overflow: hidden; /* Oculta el contenido que desborda */
  text-overflow: ellipsis; /* Muestra puntos suspensivos si el texto es demasiado largo */
}

/* Estilo para mantener siempre activo el item 'Cambiar Contraseña' */
.change-active {
  color: rgba(250, 210, 1, 0.9) !important; /* Color del texto y del icono */
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
