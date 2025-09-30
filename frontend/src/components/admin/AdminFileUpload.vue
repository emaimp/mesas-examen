<template>
  <v-card class="mx-auto" max-width="500">
    <v-card-text>
      <v-file-upload
        v-model="selectedFile"
        accept=".xlsx,.csv"
        clearable
        density="default"
        :disabled="uploading"
        label="Seleccionar archivo .xlsx o .csv"
        :loading="uploading"
        prepend-icon="mdi-microsoft-excel"
        show-size
        @click:clear="clearFile"
      />
    </v-card-text>
    <v-card-actions class="mb-2 mx-2">
      <v-btn
        block
        class="action-button"
        :disabled="!selectedFile || uploading"
        :loading="uploading"
        variant="outlined"
        @click="handleFileUpload"
      >
        Subir Excel
      </v-btn>
    </v-card-actions>
  </v-card>

  <v-snackbar
    v-model="snackbar.show"
    class="centered-snackbar"
    :color="snackbar.color"
    timeout="9000"
  >
    {{ snackbar.message }}
    <template v-if="snackbar.errors">
      <ul>
        <li v-for="(error, i) in snackbar.errors" :key="i">{{ error }}</li>
      </ul>
    </template>
  </v-snackbar>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { useFileUpload } from '../../services/admin/useFileUpload.js'

  // Inicializa el servicio de subida de archivos
  const fileUploadService = useFileUpload()

  // Variables reactivas para controlar el estado del componente
  const selectedFile = ref(null) // Almacena el archivo seleccionado para subir
  const uploading = ref(false) // Indica si un archivo se está subiendo
  const currentUploadType = ref(null) // Almacena el tipo de archivo que se está subiendo (ej. 'grades', 'users')
  const snackbar = ref({ // Objeto para controlar el snackbar de notificaciones
    show: false,
    message: '',
    color: '',
    errors: null,
  })

  // Función principal para manejar la subida del archivo
  const handleFileUpload = async () => {
    // Si no hay archivo seleccionado, muestra una advertencia
    if (!selectedFile.value) {
      snackbar.value = {
        show: true,
        message: 'Por favor, selecciona un archivo antes de subirlo.',
        color: 'warning',
        errors: null,
      }
      return
    }

    uploading.value = true // Activa el estado de subida
    snackbar.value.show = false // Oculta cualquier snackbar anterior

    try {
      let result = null
      // Llama a la función de subida correspondiente según el tipo de archivo
      switch (currentUploadType.value) {
        case 'grades': {
          result = await fileUploadService.uploadGradesXLSX(selectedFile.value)
          break
        }
        case 'users': {
          result = await fileUploadService.uploadUsersXLSX(selectedFile.value)
          break
        }
        case 'institute': {
          result = await fileUploadService.uploadPlanEstudiosXLSX(selectedFile.value)
          break
        }
        default: {
          throw new Error('Tipo de carga no definido o no soportado. Esto no debería ocurrir.')
        }
      }

      // Muestra el resultado de la subida en el snackbar
      snackbar.value = {
        show: true,
        message: result.message,
        color: result.success ? 'success' : 'error',
        errors: result.errors,
      }
    } catch (error) {
      // Manejo de errores inesperados durante la subida
      console.error('Error inesperado al intentar subir el archivo:', error)
      snackbar.value = {
        show: true,
        message: 'Ocurrió un error inesperado en la aplicación al subir el archivo.',
        color: 'error',
        errors: null,
      }
    } finally {
      // Restablece el estado después de la subida (éxito o error)
      uploading.value = false
      clearFile() // Limpia el archivo seleccionado
    }
  }

  // Función para limpiar el archivo seleccionado
  const clearFile = () => {
    selectedFile.value = null
  }

  // Observador que reacciona a la selección de un archivo para determinar el tipo de carga.
  watch(selectedFile, newFile => {
    if (newFile) {
      const fileName = newFile.name.toLowerCase()
      if (fileName.includes('notas')) {
        currentUploadType.value = 'grades'
      } else if (fileName.includes('usuarios')) {
        currentUploadType.value = 'users'
      } else if (fileName.includes('plan_estudios')) {
        currentUploadType.value = 'institute'
      } else {
        currentUploadType.value = null // No se pudo determinar el tipo
      }
    } else {
      currentUploadType.value = null
    }
  })
</script>

<style scoped>
/* Deshabilita los eventos de puntero */
.pointer-events-none {
  pointer-events: none;
}
/* Habilita los eventos de puntero */
.pointer-events-initial {
  pointer-events: initial;
}

/* Estilo para centrar el snackbar */
.centered-snackbar {
  left: 50% !important; /* Posiciona el snackbar al 50% desde la izquierda */
  transform: translateX(-50%) !important; /* Compensa el 50% de su propio ancho para centrarlo */
  text-align: center; /* Centra el texto dentro del snackbar */
}
</style>
