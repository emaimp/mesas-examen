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
        <div v-else>
          <v-row class="my-0" justify="space-around">
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="green_color"
                :value="predictionData.promocionados_percentage"
              />
              <p class="mt-2">Promocionados</p>
              <p class="mt-1">({{ predictionData.promocionados_count }} notas)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="yellow_color"
                :value="predictionData.regulares_percentage"
              />
              <p class="mt-2">Regulares</p>
              <p class="mt-1">({{ predictionData.regulares_count }} notas)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="red_color"
                :value="predictionData.libres_percentage"
              />
              <p class="mt-2">Libres</p>
              <p class="mt-1">({{ predictionData.libres_count }} notas)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-5">
            <p><strong>Total de notas evaluadas: {{ predictionData.total_notas_evaluadas }}</strong></p>
          </div>
        </div>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
  import { useAdminDashboardStore } from '@/stores/adminDashboard'
  import PercentageCircle from './PercentageCircle.vue'

  const props = defineProps({
    careerId: {
      type: Number,
      required: false,
    },
  })

  // Inicializa el store de dashboard admin
  const adminDashboardStore = useAdminDashboardStore()

  // Función para cargar predicción usando el store con cache
  const loadPrediction = async careerId => {
    await adminDashboardStore.fetchGlobalPrediction(careerId)
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadPrediction(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar al template
  const predictionData = computed(() => adminDashboardStore.globalPrediction || {
    carrera_id: null,
    carrera_nombre: 'Selecciona una carrera',
    promocionados_count: 0,
    promocionados_percentage: 0,
    regulares_count: 0,
    regulares_percentage: 0,
    libres_count: 0,
    libres_percentage: 0,
    total_notas_evaluadas: 0,
  })
  const loading = computed(() => adminDashboardStore.isLoadingPrediction)
  const error = computed(() => adminDashboardStore.predictionError)
</script>

<style scoped>

</style>
