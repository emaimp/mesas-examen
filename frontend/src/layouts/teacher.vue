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
          link
          prepend-icon="mdi-account-details"
          title="Perfil"
          :to="user ? '/teacher/' + encodeURIComponent(user.nombre) + '/profile' : ''"
          value="teacher-profile"
          @click="appStore.setSelectedSection('teacher-profile')"
        />

        <v-list-item
          link
          prepend-icon="mdi-account-school"
          title="Estudiantes Asignados"
          :to="user ? `/teacher/${encodeURIComponent(user.nombre)}/students-subject` : ''"
          value="students-subject"
          @click="appStore.setSelectedSection('students-subject')"
        />

        <v-list-item
          link
          prepend-icon="mdi-calendar-check"
          title="Mesas Examen Asignadas"
          :to="user ? `/teacher/${encodeURIComponent(user.nombre)}/tables-assigned` : ''"
          value="tables-assigned"
          @click="appStore.setSelectedSection('tables-assigned')"
        />

        <v-list-item
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
          @click="logout"
        />
      </v-list>
    </v-navigation-drawer>

    <v-main class="d-flex flex-grow-1 align-center justify-center">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
  import { useAuthUser } from '@/services/user/useAuthUser'
  import { useAppStore } from '@/stores/app' // Store de Pinia para la gestión del estado de la aplicación

  // Estado reactivo para controlar la visibilidad del menú lateral
  const drawer = ref(true)
  // Inicializa el store de la aplicación
  const appStore = useAppStore()
  // Inicializa el enrutador de Vue
  const router = useRouter()
  // Desestructura propiedades del servicio de autenticación de usuario
  const { user, fetchAuthUser } = useAuthUser()

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
  onMounted(() => {
    // Verifica si existe un token de acceso
    if (localStorage.getItem('access_token')) {
      fetchAuthUser() // Si existe, intenta obtener los datos del usuario
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
/* Estilos para el subtítulo del email en el menú */
.email-subtitle {
  font-size: 0.70rem; /* Tamaño de fuente reducido */
  white-space: nowrap; /* Evita el salto de línea */
  overflow: hidden; /* Oculta el contenido que desborda */
  text-overflow: ellipsis; /* Muestra puntos suspensivos si el texto es demasiado largo */
}

/* Estilo para mantener siempre activo el item 'Cerrar Sesión' */
.logout-active {
  background-color: rgba(128, 0, 0, 0.2) !important; /* Color de fondo con opacidad */
  color: #800000 !important; /* Color del texto y del icono */
}

/* Asegura que el icono de 'Cerrar Sesión' también tome el color correcto */
.logout-active .v-icon {
  color: #800000 !important;
}
</style>
