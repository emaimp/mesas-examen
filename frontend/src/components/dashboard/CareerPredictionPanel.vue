<template>
  <v-card class="pa-4">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando predicción de rendimiento...</p>
        </div>
        <div v-else-if="error" class="text-center text-red">
          <p>{{ error }}</p>
        </div>
        <div v-else-if="!predictionData || predictionData.total_notas_evaluadas === 0" class="text-center">
          <p>No hay datos de predicción disponibles.</p>
        </div>
        <div v-else>
          <v-row class="my-0" justify="space-around">
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="green_color"
                :value="predictionData.promocionados_percentage"
              />
              <p class="mt-2">Promocionados ({{ predictionData.promocionados_count }} notas)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="yellow_color"
                :value="predictionData.regulares_percentage"
              />
              <p class="mt-2">Regulares ({{ predictionData.regulares_count }} notas)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="red_color"
                :value="predictionData.libres_percentage"
              />
              <p class="mt-2">Libres ({{ predictionData.libres_count }} notas)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-6">
            <p><strong>Total de notas evaluadas: {{ predictionData.total_notas_evaluadas }}</strong></p>
          </div>
        </div>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
  import { watch } from 'vue'
  import { usePredictionPerformance } from '@/services/admin/usePredictionPerformance'
  import PercentageCircle from './PercentageCircle.vue'

  const props = defineProps({
    careerId: {
      type: Number,
      required: false,
    },
  })

  // Inicializa el servicio para obtener la predicción de rendimiento
  const { fetchPredictionPerformance } = usePredictionPerformance()

  // Estados reactivos
  const predictionData = ref({
    carrera_id: null,
    carrera_nombre: 'Cargando...',
    promocionados_count: 0,
    promocionados_percentage: 0,
    regulares_count: 0,
    regulares_percentage: 0,
    libres_count: 0,
    libres_percentage: 0,
    total_notas_evaluadas: 0,
  })
  const loading = ref(false)
  const error = ref(null)

  // Función para cargar predicción de rendimiento
  const loadPrediction = async careerId => {
    loading.value = true
    error.value = null
    predictionData.value.carrera_nombre = 'Cargando...'
    try {
      const data = await fetchPredictionPerformance(careerId)
      if (data) {
        predictionData.value = data
      } else {
        error.value = 'No se pudo cargar los datos de predicción de rendimiento.'
        predictionData.value.carrera_nombre = 'No encontrada'
      }
    } catch (error_) {
      error.value = error_.message || 'Ocurrió un error al cargar los datos de predicción de rendimiento.'
      predictionData.value.carrera_nombre = 'Error'
    } finally {
      loading.value = false
    }
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadPrediction(newId)
    } else {
      // Restablece valores si no hay carrera seleccionada
      predictionData.value = {
        carrera_id: null,
        carrera_nombre: 'Selecciona una carrera',
        promocionados_count: 0,
        promocionados_percentage: 0,
        regulares_count: 0,
        regulares_percentage: 0,
        libres_count: 0,
        libres_percentage: 0,
        total_notas_evaluadas: 0,
      }
      loading.value = false
      error.value = null
    }
  }, { immediate: true })
</script>

<style scoped>

</style>
