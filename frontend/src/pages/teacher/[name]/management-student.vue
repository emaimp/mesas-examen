<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" lg="4" md="4">
        <v-card class="pa-4">
          <v-card-title class="text-h5 mb-6 text-center pt-7">
            Buscar Estudiante
          </v-card-title>
          <v-card-text>
            <div class="d-flex justify-center mb-4">
              <v-img
                alt="Logo de la Aplicación"
                contain
                max-width="120"
                src="@/assets/student.png"
              />
            </div>
            <v-card-text>
              <CareerAutocomplete
                v-model="selectedCareerId"
                class="mb-4"
                label="Seleccione una Carrera"
              />

              <StudentAutocomplete
                v-model="selectedStudentId"
                :career-id="selectedCareerId"
                class="mb-4"
                label="Seleccione un Estudiante"
                @student-data-selected="handleStudentDataSelected"
              />

              <v-btn
                block
                class="mt-4 action-button"
                :disabled="!selectedCareerId || !selectedStudentId"
                variant="outlined"
                @click="handleInscripcion"
              >
                Buscar Estudiante
              </v-btn>
            </v-card-text>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import CareerAutocomplete from '../../../components/autocomplete/CareerAutocomplete.vue'
  import StudentAutocomplete from '../../../components/autocomplete/StudentAutocomplete.vue'

  // Inicializa el enrutador de Vue
  const router = useRouter()
  const route = useRoute() // Añadir esta línea para obtener la ruta actual
  // Estado reactivo para la fuente del logo
  // Estado reactivo para el ID de la carrera seleccionada
  const selectedCareerId = ref(null)
  // Estado reactivo para el ID del estudiante seleccionado
  const selectedStudentId = ref(null)
  // Estado reactivo para los datos completos del estudiante seleccionado
  const selectedStudentFullData = ref(null)

  // Observa cambios en el ID de la carrera seleccionada
  watch(selectedCareerId, () => {
    // Cuando la carrera cambia, reinicia el estudiante seleccionado
    selectedStudentId.value = null
    selectedStudentFullData.value = null
  })

  /**
   * Maneja la selección de datos de un estudiante en el autocompletado
   * @param {Object} studentData - Los datos completos del estudiante seleccionado
   */
  const handleStudentDataSelected = studentData => {
    selectedStudentFullData.value = studentData
  }

  /**
   * Maneja la acción de buscar estudiante y redirige a su perfil
   */
  const handleInscripcion = () => {
    // Verifica que se hayan seleccionado una carrera, un estudiante y sus datos
    if (selectedCareerId.value && selectedStudentId.value && selectedStudentFullData.value) {
      // Obtener el nombre del profesor de la ruta actual
      const teacherName = route.params.name

      // Redirige a la página de perfil del estudiante usando su ID y el nombre del profesor
      router.push({
        name: '/teacher/student/[id]/digital-acts',
        params: {
          name: teacherName, // Añadir el parámetro 'name'
          id: selectedStudentFullData.value.id,
        },
      })
    } else {
      // Muestra una alerta si faltan datos
      alert('Por favor, seleccione una carrera y un estudiante para continuar.')
    }
  }
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: teacher
</route>
