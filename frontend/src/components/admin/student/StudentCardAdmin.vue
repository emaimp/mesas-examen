<template>
  <v-card class="student-card" :disabled="loading" :loading="loading">
    <v-card-title class="text-h5 text-center">
      {{ student ? student.carrera_nombre || 'Detalles del Estudiante' : 'Detalles del Estudiante' }}
    </v-card-title>
    <v-card-text>
      <div v-if="student" class="mt-9">
        <v-row dense>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Nombre:</v-list-item-title>
              <v-list-item-subtitle>{{ student.nombre }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">DNI:</v-list-item-title>
              <v-list-item-subtitle>{{ student.dni }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Libreta:</v-list-item-title>
              <v-list-item-subtitle>{{ student.libreta || 'N/A' }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Email:</v-list-item-title>
              <v-list-item-subtitle>{{ student.email || 'N/A' }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>
      </div>
      <v-alert v-else-if="!loading && !studentId" text="Seleccione un estudiante para ver sus detalles." type="info" />
      <v-alert v-else-if="!loading && !student" text="No se encontraron datos para el estudiante." type="warning" />
    </v-card-text>
  </v-card>
</template>

<script setup>
  import { useStudentSearch } from '../../../services/student/useStudentSearch'

  // Define las propiedades que este componente puede recibir
  const props = defineProps({
    studentId: {
      type: [Number, String],
      required: true, // studentId es una propiedad requerida
    },
  })

  // Obtiene la función para buscar estudiante por ID del servicio
  const { fetchStudentById } = useStudentSearch()

  // Variables reactivas para almacenar los datos del estudiante y el estado de carga
  const student = ref(null) // Almacena los datos del estudiante
  const loading = ref(false) // Indica si los datos están cargando

  // Función para cargar los datos del estudiante
  const loadStudentData = async id => {
    // Si no hay ID, resetea los datos y el estado de carga
    if (!id) {
      student.value = null
      loading.value = false
      return
    }
    loading.value = true // Inicia el estado de carga
    try {
      student.value = await fetchStudentById(id) // Carga los datos del estudiante
    } catch (error) {
      console.error('Error al cargar los datos del estudiante:', error)
      student.value = null // En caso de error, resetea los datos
    } finally {
      loading.value = false // Finaliza el estado de carga
    }
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(() => {
    loadStudentData(props.studentId) // Carga los datos iniciales del estudiante
  })

  // Observa cambios en la propiedad studentId y recarga los datos
  watch(() => props.studentId, newId => {
    loadStudentData(newId)
  }, { immediate: true }) // Carga los datos inmediatamente al iniciar el componente
</script>

<style scoped>
/* Estilos específicos para la tarjeta del estudiante */
.student-card {
  margin: 16px; /* Margen alrededor de la tarjeta */
  padding: 16px; /* Relleno dentro de la tarjeta */
}
</style>
