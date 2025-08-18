<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" lg="4" md="4">
        <v-card class="pa-7">
          <v-card-title class="text-h5 mb-7 text-center">
            Crear Mesa de Examen
          </v-card-title>
          <v-card-text>

            <div v-if="loading" class="text-center py-5">
              <v-progress-circular color="primary" indeterminate />
              <p class="mt-2 text-white">Cargando...</p>
            </div>

            <CareerAutocomplete
              v-model="selectedCareerId"
              class="mb-4"
              label="Carrera"
            />

            <SubjectAutocomplete
              v-model="selectedSubjectId"
              :career-id="selectedCareerId"
              class="mb-4"
              label="Materia"
            />

            <TeacherAutocomplete
              v-model="selectedProfessorId"
              :career-id="selectedCareerId"
              class="mb-4"
              label="Profesor"
            />

            <DateTimePicker
              v-model="selectedDateTime"
              class="mb-4"
              label="Fecha y Hora"
            />

            <v-btn
              block
              class="mt-4 action-button"
              :disabled="!selectedSubjectId || !selectedProfessorId"
              variant="outlined"
              @click="handlecreateTable"
            >
              CREAR MESA
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar.show"
      class="centered-snackbar"
      :color="snackbar.color"
      timeout="6000"
    >
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
  import DateTimePicker from '../../components/admin/DateTimePicker.vue'
  import CareerAutocomplete from '../../components/autocomplete/CareerAutocomplete.vue'
  import SubjectAutocomplete from '../../components/autocomplete/SubjectAutocomplete.vue'
  import TeacherAutocomplete from '../../components/autocomplete/TeacherAutocomplete.vue'
  import { useCrearMesa } from '../../services/admin/useCreateTable'

  // Estados reactivos para los campos del formulario
  const loading = ref(false) // Estado para controlar la visibilidad del indicador de carga
  const selectedCareerId = ref(null) // ID de la carrera seleccionada
  const selectedSubjectId = ref(null) // ID de la materia seleccionada
  const selectedProfessorId = ref(null) // ID del profesor seleccionado
  const selectedDateTime = ref(null) // Fecha y hora seleccionadas

  // Estado reactivo para la barra de notificación (snackbar)
  const snackbar = ref({
    show: false, // Controla la visibilidad del snackbar
    message: '', // Mensaje a mostrar en el snackbar
    color: '', // Color del snackbar (ej. 'success', 'error', 'warning')
  })

  // Inicializa el servicio para crear mesas.
  const { createTable } = useCrearMesa()

  /**
   * Formatea un objeto Date a una cadena de fecha y hora compatible con el backend (ISO 8601 con offset)
   * @param {Date} date - El objeto Date a formatear
   * @returns {string} La cadena de fecha y hora formateada
   */
  const formatDateToBackend = date => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0') // Meses son 0-indexados
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')
    const offset = date.getTimezoneOffset() // Diferencia en minutos entre UTC y la hora local
    const offsetHours = String(Math.abs(Math.floor(offset / 60))).padStart(2, '0')
    const offsetMinutes = String(Math.abs(offset % 60)).padStart(2, '0')
    const offsetSign = offset > 0 ? '-' : '+' // Signo del offset
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}${offsetSign}${offsetHours}:${offsetMinutes}`
  }

  /**
   * Maneja la creación de una nueva mesa de examen
   */
  const handlecreateTable = async () => {
    // Valida que todos los campos requeridos estén seleccionados
    if (!selectedSubjectId.value || !selectedProfessorId.value || !selectedDateTime.value) {
      snackbar.value.message = 'Por favor, selecciona Materia, Profesor y Fecha/Hora.'
      snackbar.value.color = 'warning'
      snackbar.value.show = true
      return
    }

    let dateToFormat = selectedDateTime.value
    // Asegura que selectedDateTime.value sea un objeto Date
    if (!(dateToFormat instanceof Date)) {
      dateToFormat = new Date(selectedDateTime.value)
    }

    const formattedDate = formatDateToBackend(dateToFormat) // Formatea la fecha para el backend
    // Prepara los datos de la mesa para enviar a la API
    const mesaData = {
      materia_carrera_id: Number.parseInt(selectedSubjectId.value),
      profesor_id: Number.parseInt(selectedProfessorId.value),
      fecha: formattedDate,
    }

    loading.value = true // Muestra el indicador de carga

    try {
      // Llama al servicio para crear la mesa
      const response = await createTable(mesaData)

      // Muestra un mensaje de éxito y limpia el formulario
      snackbar.value.message = response.message || 'Mesa creada con éxito.'
      snackbar.value.color = 'success'
      selectedCareerId.value = null
      selectedSubjectId.value = null
      selectedProfessorId.value = null
      selectedDateTime.value = null
      snackbar.value.show = true
    } catch (error) {
      // Maneja errores de la API o de conexión
      if (error.response && error.response.data && error.response.data.detail) {
        snackbar.value.message = error.response.data.detail
        snackbar.value.color = 'error'
      } else {
        snackbar.value.message = 'Error de conexión o inesperado: ' + error.message
        snackbar.value.color = 'error'
      }
      snackbar.value.show = true
    } finally {
      loading.value = false // Oculta el indicador de carga
    }
  }
</script>

<style scoped>
/* Estilos para centrar la barra de notificación (snackbar) */
.centered-snackbar {
  left: 50% !important; /* Centra horizontalmente */
  transform: translateX(-50%) !important; /* Ajuste para centrado perfecto */
  text-align: center; /* Centra el texto */
}
</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
