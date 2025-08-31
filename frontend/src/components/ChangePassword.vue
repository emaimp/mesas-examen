<template>
  <!-- Tarjeta que contiene el formulario de cambio de contraseña -->
  <v-card class="elevation-12 pa-5">
    <v-card-text class="px-3 py-5">

      <img alt="IESN6 Logo" class="login-logo" src="@/assets/key.png">
      <div class="mb-8" />

      <!-- Formulario de cambio de contraseña con validación y envío -->
      <v-form ref="form" @submit.prevent="submitChangePassword">

        <!-- Campo de texto para la contraseña actual -->
        <v-text-field
          v-model="currentPassword"
          :append-inner-icon="currentPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
          autocomplete="off"
          class="mb-6"
          dense
          label="Contraseña Actual"
          outlined
          required
          :rules="[v => !!v || 'Contraseña actual requerida']"
          :type="currentPasswordVisible ? 'text' : 'password'"
          variant="outlined"
          @click:append-inner="toggleCurrentPasswordVisibility"
        />

        <!-- Campo de texto para la nueva contraseña -->
        <v-text-field
          v-model="newPassword"
          :append-inner-icon="newPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
          autocomplete="off"
          class="mb-6"
          dense
          label="Nueva Contraseña"
          outlined
          required
          :rules="[
            v => !!v || 'Nueva contraseña requerida',
            v => v.length >= 6 || 'La contraseña debe tener al menos 5 caracteres',
          ]"
          :type="newPasswordVisible ? 'text' : 'password'"
          variant="outlined"
          @click:append-inner="toggleNewPasswordVisibility"
        />

        <!-- Campo de texto para confirmar la nueva contraseña -->
        <v-text-field
          v-model="confirmNewPassword"
          :append-inner-icon="confirmNewPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
          autocomplete="off"
          class="mb-6"
          dense
          label="Confirmar Contraseña"
          outlined
          required
          :rules="[
            v => !!v || 'Confirme la nueva contraseña',
            v => v === newPassword || 'Las contraseñas no coinciden',
          ]"
          :type="confirmNewPasswordVisible ? 'text' : 'password'"
          variant="outlined"
          @click:append-inner="toggleConfirmNewPasswordVisibility"
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

        <!-- Alerta de éxito -->
        <v-alert
          v-if="successMessage"
          class="mb-1"
          dense
          outlined
          type="success"
        >
          {{ successMessage }}
        </v-alert>

        <!-- Botón para cambiar contraseña -->
        <v-btn
          block
          class="mt-6 action-button"
          :disabled="!isFormValid"
          size="large"
          type="submit"
          variant="outlined"
        >
          Cambiar Contraseña
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
  import { usePasswordChange } from '@/services/user/usePasswordChange'

  export default {
    name: 'ChangePassword',
    setup () {
      const currentPassword = ref('') // Estado para la contraseña actual
      const newPassword = ref('') // Estado para la nueva contraseña
      const confirmNewPassword = ref('') // Estado para confirmar la nueva contraseña
      const errorMessage = ref('') // Estado para mensajes de error
      const successMessage = ref('') // Estado para mensajes de éxito
      const currentPasswordVisible = ref(false) // Estado para la visibilidad de la contraseña actual
      const newPasswordVisible = ref(false) // Estado para la visibilidad de la nueva contraseña
      const confirmNewPasswordVisible = ref(false) // Estado para la visibilidad de la confirmación de contraseña

      const form = ref(null) // Referencia al formulario
      const { changePassword, loading, error, success } = usePasswordChange() // Obtiene las funciones y estados del hook

      const isFormValid = computed(() => { // Propiedad computada para validar el formulario
        return (
          currentPassword.value.trim() !== ''
          && newPassword.value.trim() !== ''
          && confirmNewPassword.value.trim() !== ''
          && newPassword.value === confirmNewPassword.value
          && newPassword.value.length >= 6
        )
      })

      const submitChangePassword = async () => { // Función asíncrona para enviar el cambio de contraseña
        const { valid } = await form.value.validate() // Llama al método validate() del formulario
        if (valid) {
          errorMessage.value = '' // Limpia mensajes de error previos
          successMessage.value = '' // Limpia mensajes de éxito previos

          try {
            await changePassword(currentPassword.value, newPassword.value) // Llama a la función de cambio de contraseña

            if (success.value) { // Si el cambio fue exitoso
              successMessage.value = 'Contraseña cambiada exitosamente.' // Muestra mensaje de éxito
              currentPassword.value = '' // Limpia el campo de contraseña actual
              newPassword.value = '' // Limpia el campo de nueva contraseña
              confirmNewPassword.value = '' // Limpia el campo de confirmación de contraseña
              form.value.resetValidation() // Resetea la validación del formulario
            } else if (error.value) { // Si hubo un error
              errorMessage.value = error.value // Muestra el mensaje de error
            }
          } catch (error_) { // Captura errores inesperados
            console.error('Error al cambiar la contraseña:', error_) // Registra el error en consola
            errorMessage.value = 'Ocurrió un error al intentar cambiar la contraseña.' // Muestra mensaje de error genérico
          }
        }
      }

      const toggleCurrentPasswordVisibility = () => { // Función para alternar la visibilidad de la contraseña actual
        currentPasswordVisible.value = !currentPasswordVisible.value
      }

      const toggleNewPasswordVisibility = () => { // Función para alternar la visibilidad de la nueva contraseña
        newPasswordVisible.value = !newPasswordVisible.value
      }

      const toggleConfirmNewPasswordVisibility = () => { // Función para alternar la visibilidad de la confirmación de contraseña
        confirmNewPasswordVisible.value = !confirmNewPasswordVisible.value
      }

      return { // Retorna los estados y funciones para usarlos en el template
        currentPassword,
        newPassword,
        confirmNewPassword,
        errorMessage,
        successMessage,
        currentPasswordVisible,
        newPasswordVisible,
        confirmNewPasswordVisible,
        isFormValid,
        submitChangePassword,
        toggleCurrentPasswordVisibility,
        toggleNewPasswordVisibility,
        toggleConfirmNewPasswordVisibility,
        loading, // Exponer loading para deshabilitar el botón si es necesario
        form, // Exponer la referencia del formulario
      }
    },
  }
</script>

<style scoped>
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

/* Estilos para el logo */
.login-logo {
  max-width: 100%; /* Ancho máximo del 100% del contenedor */
  width: 130px; /* Ancho fijo */
  height: auto; /* Altura automática para mantener la proporción */
  display: block; /* Hace que la imagen sea un bloque para centrarla */
  margin: 0 auto; /* Centra la imagen horizontalmente */
  padding: 10px 0; /* Relleno superior e inferior */
}
</style>
