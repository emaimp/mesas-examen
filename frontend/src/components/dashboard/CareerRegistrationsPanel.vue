<template>
  <v-card class="pa-4">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando inscripciones...</p>
        </div>
        <div v-else-if="error" class="text-center text-red">
          <p>{{ error }}</p>
        </div>
        <div v-else-if="!registrationsData || registrationsData.total_inscripciones === 0" class="text-center">
          <p>No hay datos de inscripciones disponibles.</p>
        </div>
        <div v-else>
          <v-row class="my-0" justify="space-around">
            <v-col class="text-center" cols="12" sm="6">
              <PercentageCircle
                color="green_color"
                :value="registrationsData.activos_percentage"
              />
              <p class="mt-2">Activas ({{ registrationsData.activos_count }} inscripciones)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="6">
              <PercentageCircle
                color="red_color"
                :value="registrationsData.cancelados_percentage"
              />
              <p class="mt-2">Canceladas ({{ registrationsData.cancelados_count }} inscripciones)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-6">
            <p><strong>Total de inscripciones: {{ registrationsData.total_inscripciones }}</strong></p>
          </div>
        </div>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
  import { watch } from 'vue'
  import { useGlobalRegistrations } from '@/services/admin/useGlobalRegistrations'
  import PercentageCircle from './PercentageCircle.vue'

  const props = defineProps({
    careerId: {
      type: Number,
      required: false,
    },
  })

  // Inicializa el servicio para obtener las registros globales
  const { fetchGlobalRegistrations } = useGlobalRegistrations()

  // Estados reactivos
  const registrationsData = ref({
    carrera_id: null,
    carrera_nombre: 'Cargando...',
    activos_count: 0,
    activos_percentage: 0,
    cancelados_count: 0,
    cancelados_percentage: 0,
    total_inscripciones: 0,
  })
  const loading = ref(false)
  const error = ref(null)

  // Función para cargar registros
  const loadRegistrations = async careerId => {
    loading.value = true
    error.value = null
    registrationsData.value.carrera_nombre = 'Cargando...'
    try {
      const data = await fetchGlobalRegistrations(careerId)
      if (data) {
        registrationsData.value = data
      } else {
        error.value = 'No se pudo cargar los datos de inscripciones.'
        registrationsData.value.carrera_nombre = 'No encontrada'
      }
    } catch (error_) {
      error.value = error_.message || 'Ocurrió un error al cargar los datos de inscripciones.'
      registrationsData.value.carrera_nombre = 'Error'
    } finally {
      loading.value = false
    }
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadRegistrations(newId)
    } else {
      // Restablece valores si no hay carrera seleccionada
      registrationsData.value = {
        carrera_id: null,
        carrera_nombre: 'Selecciona una carrera',
        activos_count: 0,
        activos_percentage: 0,
        cancelados_count: 0,
        cancelados_percentage: 0,
        total_inscripciones: 0,
      }
      loading.value = false
      error.value = null
    }
  }, { immediate: true })
</script>

<style scoped>

</style>
