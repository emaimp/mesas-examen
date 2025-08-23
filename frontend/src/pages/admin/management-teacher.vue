<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" lg="4" md="4">
        <v-card class="pa-4">
          <v-card-title class="text-h5 mb-6 text-center pt-7">
            Gestión de Profesor
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

              <TeacherAutocomplete
                v-model="selectedTeacherId"
                :career-id="selectedCareerId"
                class="mb-4"
                label="Seleccione un Profesor"
                @teacher-data-selected="handleTeacherDataSelected"
              />

              <v-btn
                block
                class="mt-4 action-button"
                :disabled="!selectedCareerId || !selectedTeacherId"
                variant="outlined"
                @click="handleSearchTeacher"
              >
                Buscar Profesor
              </v-btn>
            </v-card-text>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>cle
  </v-container>
</template>

<script setup>
  import CareerAutocomplete from '../../components/autocomplete/CareerAutocomplete.vue'
  import TeacherAutocomplete from '../../components/autocomplete/TeacherAutocomplete.vue'

  // Inicializa el enrutador de Vue
  const router = useRouter()
  // Estado reactivo para el ID de la carrera seleccionada
  const selectedCareerId = ref(null)
  // Estado reactivo para el ID del profesor seleccionado
  const selectedTeacherId = ref(null)
  // Estado reactivo para los datos completos del profesor seleccionado
  const selectedTeacherFullData = ref(null)

  // Observa cambios en el ID de la carrera seleccionada
  watch(selectedCareerId, () => {
    // Cuando la carrera cambia, reinicia el profesor seleccionado
    selectedTeacherId.value = null
    selectedTeacherFullData.value = null
  })

  /**
   * Maneja la selección de datos de un profesor en el autocompletado
   * @param {Object} teacherData - Los datos completos del profesor seleccionado
   */
  const handleTeacherDataSelected = teacherData => {
    selectedTeacherFullData.value = teacherData
  }

  /**
   * Maneja la acción de buscar profesor y redirige a su perfil
   */
  const handleSearchTeacher = () => {
    // Verifica que se hayan seleccionado una carrera, un profesor y sus datos
    if (selectedCareerId.value && selectedTeacherId.value && selectedTeacherFullData.value) {
      // Redirige a la página de perfil del profesor usando su ID
      router.push({
        name: '/admin/teacher/[id]/profile',
        params: {
          id: selectedTeacherFullData.value.id,
        },
      })
    } else {
      // Muestra una alerta si faltan datos
      alert('Por favor, seleccione una carrera y un profesor para continuar.')
    }
  }
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
