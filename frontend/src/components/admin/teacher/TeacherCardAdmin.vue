<template>
  <v-card class="teacher-card" :disabled="loading" :loading="loading">
    <v-card-title class="text-h5 text-center">
      {{ teacher ? teacher.carrera_nombre || 'Detalles del Profesor' : 'Detalles del Profesor' }}
    </v-card-title>
    <v-card-text>
      <div v-if="teacher" class="mt-9">
        <v-row dense>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Nombre:</v-list-item-title>
              <v-list-item-subtitle>{{ teacher.nombre }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">DNI:</v-list-item-title>
              <v-list-item-subtitle>{{ teacher.dni }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Legajo:</v-list-item-title>
              <v-list-item-subtitle>{{ teacher.legajo || 'N/A' }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Email:</v-list-item-title>
              <v-list-item-subtitle>{{ teacher.email || 'N/A' }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Carreras:</v-list-item-title>
              <v-list-item-subtitle>{{ teacher.carrera_nombre || 'N/A' }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="3">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Materias:</v-list-item-title>
              <v-list-item-subtitle>{{ teacher.materia_nombre || 'N/A' }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>
      </div>
      <v-alert v-else-if="!loading && !teacherId" text="Seleccione un profesor para ver sus detalles." type="info" />
      <v-alert v-else-if="!loading && !teacher" text="No se encontraron datos para el profesor." type="warning" />
    </v-card-text>
  </v-card>
</template>

<script setup>
  import { useTeacherSearch } from '../../../services/teacher/useTeacherSearch'

  // Define las propiedades que este componente puede recibir
  const props = defineProps({
    teacherId: {
      type: [Number, String],
      required: true, // teacherId es una propiedad requerida
    },
  })

  // Obtiene la función para buscar profesor por ID del servicio
  const { fetchTeacherById } = useTeacherSearch()

  // Variables reactivas para almacenar los datos del profesor y el estado de carga
  const teacher = ref(null) // Almacena los datos del profesor
  const loading = ref(false) // Indica si los datos están cargando

  // Función para cargar los datos del profesor
  const loadTeacherData = async id => {
    // Si no hay ID, resetea los datos y el estado de carga
    if (!id) {
      teacher.value = null
      loading.value = false
      return
    }
    loading.value = true // Inicia el estado de carga
    try {
      teacher.value = await fetchTeacherById(id) // Carga los datos del profesor
    } catch (error) {
      console.error('Error al cargar los datos del profesor:', error)
      teacher.value = null // En caso de error, resetea los datos
    } finally {
      loading.value = false // Finaliza el estado de carga
    }
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(() => {
    loadTeacherData(props.teacherId) // Carga los datos iniciales del profesor
  })

  // Observa cambios en la propiedad teacherId y recarga los datos
  watch(() => props.teacherId, newId => {
    loadTeacherData(newId)
  }, { immediate: true }) // Carga los datos inmediatamente al iniciar el componente
</script>

<style scoped>
/* Estilos específicos para la tarjeta del profesor */
.teacher-card {
  margin: 16px; /* Margen alrededor de la tarjeta */
  padding: 16px; /* Relleno dentro de la tarjeta */
}
</style>
