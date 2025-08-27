<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" lg="4" md="6" sm="8">
        <v-card class="pa-7">
          <v-card-title class="text-h5 mb-7 text-center">
            Crear Mesa de Examen
          </v-card-title>
          <v-card-text>

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

            <div class="form-section">
              <h3 class="mb-2">Primer Llamado</h3>
              <DateTimePicker
                v-model="selectedDateTime"
                class="mb-4"
                label="Fecha y Hora del primer llamado"
              />
            </div>

            <div class="form-section">
              <h3 class="mb-2">Segundo Llamado</h3>
              <DateTimePicker
                v-model="selectedDateTime2nd"
                class="mb-4"
                label="Fecha y hora del segundo llamado"
              />
            </div>

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
  const selectedCareerId = ref(null) // ID de la carrera seleccionada
  const selectedSubjectId = ref(null) // ID de la materia seleccionada
  const selectedProfessorId = ref(null) // ID del profesor seleccionado
  const selectedDateTime = ref(null) // Fecha y hora seleccionadas del primer llamado
  const selectedDateTime2nd = ref(null) // Fecha y hora seleccionadas del segundo llamado

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
    if (!selectedSubjectId.value || !selectedProfessorId.value || !selectedDateTime.value || !selectedDateTime2nd.value) {
      snackbar.value.message = 'Hay campos requeridos sin completar.'
      snackbar.value.color = 'warning'
      snackbar.value.show = true
      return
    }

    // Lógica para el primer llamado
    let dateToFormat1st = selectedDateTime.value
    // Asegura que selectedDateTime.value sea un objeto Date
    if (!(dateToFormat1st instanceof Date)) {
      dateToFormat1st = new Date(selectedDateTime.value)
    }
    const formattedDate1st = formatDateToBackend(dateToFormat1st) // Formatea la fecha para el backend
    // Prepara los datos de la mesa para enviar a la API
    const mesaData1st = {
      materia_carrera_id: Number.parseInt(selectedSubjectId.value),
      profesor_id: Number.parseInt(selectedProfessorId.value),
      fecha: formattedDate1st,
    }

    // Lógica para el segundo llamado
    let dateToFormat2nd = selectedDateTime2nd.value
    // Asegura que selectedDateTime2nd.value sea un objeto Date
    if (!(dateToFormat2nd instanceof Date)) {
      dateToFormat2nd = new Date(selectedDateTime2nd.value)
    }
    const formattedDate2nd = formatDateToBackend(dateToFormat2nd) // Formatea la fecha para el backend
    // Prepara los datos de la mesa para enviar a la API
    const mesaData2nd = {
      materia_carrera_id: Number.parseInt(selectedSubjectId.value),
      profesor_id: Number.parseInt(selectedProfessorId.value),
      fecha: formattedDate2nd,
    }

    try {
      // Llama al servicio para crear la primera mesa
      const response1st = await createTable(mesaData1st)
      // Llama al servicio para crear la segunda mesa
      const response2nd = await createTable(mesaData2nd)

      // Muestra un mensaje de éxito y limpia el formulario
      snackbar.value.message = `Primer llamado: ${response1st.message || 'Creado con éxito.'} Segundo llamado: ${response2nd.message || 'Creado con éxito.'}`
      snackbar.value.color = 'success'
      selectedCareerId.value = null
      selectedSubjectId.value = null
      selectedProfessorId.value = null
      selectedDateTime.value = null
      selectedDateTime2nd.value = null
      snackbar.value.show = true
    } catch (error) {
      // Maneja errores de la API o de conexión para ambas llamadas
      let errorMessage = '' // Inicializa el mensaje de error vacío
      // Reemplaza el if/else con un operador ternario para el mensaje de error
      errorMessage = (error.response && error.response.data && error.response.data.detail) ? error.response.data.detail : 'Error: ' + error.message
      snackbar.value.message = errorMessage
      snackbar.value.color = 'error'
      snackbar.value.show = true
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
