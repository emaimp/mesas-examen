<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col lg="4">
        <v-card class="pa-4">
          <v-card-text>

            <CareerAutocomplete
              v-model="selectedCareerId"
              class="mt-1 mb-10"
              label="Carrera"
            />

            <SubjectAutocomplete
              v-model="selectedSubjectId"
              :career-id="selectedCareerId"
              class="mb-10"
              label="Materia"
            />

            <TeacherAutocomplete
              v-model="selectedProfessorId"
              :career-id="selectedCareerId"
              class="mb-8"
              label="Profesor"
            />

            <div class="form-section">
              <h3 class="mb-2">Primer Llamado</h3>
              <DateTimePicker
                v-model="selectedDateTime"
                label="Fecha y Hora del primer llamado"
              />
            </div>

            <div class="form-section">
              <h3 class="mb-2">Segundo Llamado</h3>
              <DateTimePicker
                v-model="selectedDateTime2nd"
                class="mb-1"
                label="Fecha y hora del segundo llamado"
              />
            </div>

            <v-btn
              block
              class="action-button"
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
  import { useAdminTablesStore } from '../../stores/adminTables.js'

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

  // Inicializa el store de adminTables para notificaciones de cambios
  const adminTablesStore = useAdminTablesStore()

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
    // 1. Ajustar la validación inicial
    if (!selectedSubjectId.value || !selectedProfessorId.value || (!selectedDateTime.value && !selectedDateTime2nd.value)) {
      snackbar.value.message = 'Debe seleccionar una materia, un profesor y al menos una fecha de llamado.'
      snackbar.value.color = 'warning'
      snackbar.value.show = true
      return
    }

    const successMessages = []
    const errorMessages = []

    // 2. Lógica para el primer llamado (si está presente)
    if (selectedDateTime.value) {
      let dateToFormat1st = selectedDateTime.value
      // Asegura que la fecha sea un objeto Date
      if (!(dateToFormat1st instanceof Date)) {
        dateToFormat1st = new Date(selectedDateTime.value)
      }
      // Formatea la fecha para el backend
      const formattedDate1st = formatDateToBackend(dateToFormat1st)

      // Prepara los datos para el primer llamado
      const mesaData1st = {
        materia_carrera_id: Number.parseInt(selectedSubjectId.value),
        profesor_id: Number.parseInt(selectedProfessorId.value),
        primer_llamado: formattedDate1st,
        segundo_llamado: null, // El segundo llamado es nulo para el primer llamado
      }
      try {
        // Intenta crear la mesa para el primer llamado
        await createTable(mesaData1st)
        successMessages.push('Primer llamado creado con éxito.')
      } catch (error) {
        // Captura y almacena mensajes de error
        errorMessages.push(`Error al crear el primer llamado: ${error.response?.data?.detail || error.message}`)
      }
    }

    // 3. Lógica para el segundo llamado (si está presente)
    if (selectedDateTime2nd.value) {
      let dateToFormat2nd = selectedDateTime2nd.value
      // Asegura que la fecha sea un objeto Date
      if (!(dateToFormat2nd instanceof Date)) {
        dateToFormat2nd = new Date(selectedDateTime2nd.value)
      }
      // Formatea la fecha para el backend
      const formattedDate2nd = formatDateToBackend(dateToFormat2nd)

      // Prepara los datos para el segundo llamado
      const mesaData2nd = {
        materia_carrera_id: Number.parseInt(selectedSubjectId.value),
        profesor_id: Number.parseInt(selectedProfessorId.value),
        primer_llamado: null, // Explícitamente nulo para este llamado
        segundo_llamado: formattedDate2nd,
      }
      try {
        // Intenta crear la mesa para el segundo llamado
        await createTable(mesaData2nd)
        successMessages.push('Segundo llamado creado con éxito.')
      } catch (error) {
        // Captura y almacena mensajes de error
        errorMessages.push(`Error al crear el segundo llamado: ${error.response?.data?.detail || error.message}`)
      }
    }

    // 4. Mostrar resultados combinados
    if (successMessages.length > 0) {
      // Muestra mensajes de éxito
      snackbar.value.message = successMessages.join(' ')
      snackbar.value.color = 'success'
      // Limpia los campos del formulario si hubo éxito
      selectedCareerId.value = null
      selectedSubjectId.value = null
      selectedProfessorId.value = null
      selectedDateTime.value = null
      selectedDateTime2nd.value = null
      // Notifica cambio en el store para actualizar otras vistas
      adminTablesStore.notifyChange()
    } else {
      // Muestra mensajes de error
      snackbar.value.message = errorMessages.join(' ') || 'Error desconocido al crear las mesas.'
      snackbar.value.color = 'error'
    }
    // Muestra el snackbar
    snackbar.value.show = true
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
