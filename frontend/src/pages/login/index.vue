<template>
  <!-- Contenedor principal del formulario de identificación -->
  <v-container class="identification-form-container gradient-background" fill-height fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" lg="8" md="8" sm="8">
        <!-- Tarjeta que contiene el formulario de login -->
        <v-card class="elevation-12 pa-5">
          <img alt="IESN6 Logo" class="login-logo" src="@/assets/iesn6_icon.png">
          <v-card-text class="px-3 py-5">

            <p class="mb-8 text-center">Ingresa tu usuario y contraseña.</p>

            <!-- Formulario de login con validación y envío -->
            <v-form ref="loginForm" @submit.prevent="submitLogin">

              <!-- Campo de texto para el usuario -->
              <v-text-field
                v-model="username"
                autocomplete="off"
                class="mb-6"
                dense
                label="Usuario"
                outlined
                required
                :rules="[v => !!v || 'El usuario es requerido']"
                variant="outlined"
              />
              <!-- Campo de texto para la contraseña -->
              <v-text-field
                v-model="password"
                :append-inner-icon="passwordVisible ? 'mdi-eye-off' : 'mdi-eye'"
                autocomplete="off"
                class="mb-6"
                dense
                label="Contraseña"
                outlined
                required
                :rules="[v => !!v || 'La contraseña es requerida']"
                :type="passwordVisible ? 'text' : 'password'"
                variant="outlined"
                @click:append-inner="togglePasswordVisibility"
              />

              <!-- Alerta de mensajes de errores -->
              <v-alert
                v-if="errorMessage"
                class="mb-1"
                dense
                outlined
                type="error"
              >
                {{ errorMessage }}
              </v-alert>

              <!-- Botón de ingreso al sistema -->
              <v-btn
                block
                class="mt-6 action-button"
                :disabled="!isFormValid"
                size="large"
                type="submit"
                variant="outlined"
              >
                Ingresar
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card> </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios' // Para realizar peticiones HTTP
  import { jwtDecode } from 'jwt-decode' // Para decodificar tokens JWT
  import { useAppStore } from '@/stores/app' // Store de Pinia para la gestión del estado de la aplicación

  export default {
    name: 'IdentificationForm',
    data () {
      return {
        username: '', // Almacena el nombre de usuario
        password: '', // Almacena la contraseña
        errorMessage: '', // Almacena mensajes de error
        passwordVisible: false, // Controla la visibilidad de la contraseña
      }
    },
    computed: {
      // Valida si el formulario es válido (campos no vacíos)
      isFormValid () {
        return this.username.trim() !== '' && this.password.trim() !== ''
      },
    },
    methods: {
      /**
       * Maneja el envío del formulario de login
       */
      async submitLogin () {
        // Valida el formulario usando las reglas de Vuetify
        if (this.$refs.loginForm.validate()) {
          this.errorMessage = '' // Limpia cualquier mensaje de error previo

          try {
            // Realiza una petición POST para obtener el token de autenticación
            const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/token`, new URLSearchParams({
              username: this.username,
              password: this.password,
            }), {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
            })

            const { access_token } = response.data // Extrae el token de acceso
            localStorage.setItem('access_token', access_token) // Guarda el token en el almacenamiento local
            const decodedToken = jwtDecode(access_token) // Decodifica el token para obtener los datos del usuario
            const userRole = decodedToken.role // Obtiene el rol del usuario
            const appStore = useAppStore() // Accede al store de la aplicación
            appStore.setUser(decodedToken) // Establece los datos del usuario en el store

            // Redirige al usuario según su rol
            switch (userRole) {
              case 'student': {
                this.$router.push({
                  name: 'student',
                  params: {
                    name: decodedToken.nombre,
                  },
                })
                break
              }
              case 'teacher': {
                this.$router.push({
                  name: 'teacher',
                  params: {
                    name: decodedToken.nombre,
                  },
                })
                break
              }
              case 'admin': {
                this.$router.push({ name: 'admin' })
                break
              }
              default: {
                this.errorMessage = 'Rol de usuario desconocido. Contacta al administrador.'
                localStorage.removeItem('access_token') // Elimina el token si el rol es desconocido
                break
              }
            }
          } catch (error) {
            console.error('Error al iniciar sesión:', error)
            // Muestra un mensaje de error específico si las credenciales son incorrectas
            this.errorMessage = (error.response && error.response.status === 401)
              ? 'Usuario o contraseña incorrectos.'
              : 'Ocurrió un error al intentar iniciar sesión.'
          }
        }
      },
      /**
       * Alterna la visibilidad de la contraseña
       */
      togglePasswordVisibility () {
        this.passwordVisible = !this.passwordVisible
      },
    },
  }
</script>

<style scoped>
/* Estilos para el contenedor principal del formulario de identificación */
.identification-form-container {
  min-height: 100vh; /* Altura mínima del 100% del viewport */
  display: flex; /* Usa flexbox para centrar el contenido */
  align-items: center; /* Centra verticalmente */
  justify-content: center; /* Centra horizontalmente */
}

/* Estilos para la tarjeta del formulario */
.v-card {
  padding-bottom: 10px; /* Relleno inferior */
  border-radius: 8px; /* Bordes redondeados */
  margin-left: auto; /* Centra la tarjeta horizontalmente */
  margin-right: auto; /* Centra la tarjeta horizontalmente */
  max-width: 450px; /* Ancho máximo de la tarjeta */
  width: 100%; /* Ancho completo dentro del contenedor */
  display: block; /* Asegura que la tarjeta se comporte como un bloque */
}

/* Estilos para el logo de login */
.login-logo {
  max-width: 100%; /* Ancho máximo del 100% del contenedor */
  width: 340px; /* Ancho fijo */
  height: auto; /* Altura automática para mantener la proporción */
  display: block; /* Hace que la imagen sea un bloque para centrarla */
  margin: 0 auto; /* Centra la imagen horizontalmente */
  padding: 10px 0; /* Relleno superior e inferior */
}
</style>
