<template>
  <v-container class="fill-height gradient-background py-9" fluid>
    <v-row align="center" class="fill-height" justify="center">
      <v-col
        cols="12"
        lg="9"
        md="9"
        sm="9"
        xl="9"
      >
        <v-card class="mx-auto pa-7 transparent-card" flat :loading="loading">
          <StudentCard v-if="studentId" :student-id="studentId" />
          <v-card-text>
            <div v-if="loading" class="text-center py-5">
              <v-progress-circular color="primary" indeterminate />
              <p class="mt-2 text-white">Cargando datos del estudiante...</p>
            </div>
            <v-row v-else-if="studentId" align="start" class="mt-12" dense>
              <v-col class="mb-md-1 mb-6" cols="12">
                <NotasEstudiantePanel :student-id="studentId" />
              </v-col>
            </v-row>
            <v-alert
              v-else
              class="mb-4"
              text="ID del estudiante no encontrado en la ruta."
              type="info"
              variant="tonal"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import StudentCard from '../../../../components/admin/student/StudentCardAdmin.vue'
  import NotasEstudiantePanel from '../../../../components/admin/student/StudentNotesPanel.vue'
  import { useStudentSearch } from '../../../../services/student/useStudentSearch'

  // Obtiene la ruta actual
  const route = useRoute()
  // Inicializa el servicio de búsqueda de estudiantes
  const { fetchStudentById } = useStudentSearch()

  // Estados reactivos para los datos del estudiante
  const studentId = ref(null) // ID del estudiante obtenido de la ruta
  const studentCarreraId = ref(null) // ID de la carrera del estudiante
  const studentCarreraName = ref('') // Nombre de la carrera del estudiante
  const loading = ref(true) // Indica si los datos están cargando

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(async () => {
    studentId.value = route.params.id // Obtiene el ID del estudiante de los parámetros de la ruta

    if (studentId.value) {
      loading.value = true // Activa el estado de carga
      try {
        // Intenta obtener los datos del estudiante por su ID
        const studentData = await fetchStudentById(studentId.value)
        if (studentData) {
          studentCarreraId.value = studentData.carrera_id // Asigna el ID de la carrera
          studentCarreraName.value = studentData.carrera // Asigna el nombre de la carrera
        } else {
          console.warn(
            'Datos del estudiante no encontrados para el ID:',
            studentId.value,
          )
          studentCarreraId.value = null
          studentCarreraName.value = ''
        }
      } catch (error) {
        console.error(
          'Error al cargar datos básicos del estudiante o carrera:',
          error,
        )
        studentCarreraId.value = null
        studentCarreraName.value = ''
      } finally {
        loading.value = false // Desactiva el estado de carga
      }
    } else {
      loading.value = false // Desactiva la carga si no hay ID de estudiante
      console.warn(
        'ID del estudiante no encontrado en los parámetros de la ruta.',
      )
    }
  })
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
