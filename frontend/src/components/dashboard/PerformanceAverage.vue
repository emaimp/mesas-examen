<template>
  <v-card class="pa-5">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando rendimiento...</p>
        </div>
        <div v-else-if="error" class="text-center">
          <p>{{ error }}</p>
        </div>
        <div v-else>
          <v-row justify="center">
            <v-col class="text-center" xs="12" sm="6" md="4">
              <PercentageCircle
                color="green_color"
                :value="performanceData.promocionados_percentage"
              />
              <p class="mt-2 text-caption">Promocionados</p>
              <p class="mt-0 text-caption">({{ performanceData.promocionados_count }} notas)</p>
            </v-col>
            <v-col class="text-center" xs="12" sm="6" md="4">
              <PercentageCircle
                color="yellow_color"
                :value="performanceData.regulares_percentage"
              />
              <p class="mt-2 text-caption">Regulares</p>
              <p class="mt-0 text-caption">({{ performanceData.regulares_count }} notas)</p>
            </v-col>
            <v-col class="text-center" xs="12" sm="6" md="4">
              <PercentageCircle
                color="red_color"
                :value="performanceData.libres_percentage"
              />
              <p class="mt-2 text-caption">Libres</p>
              <p class="mt-0 text-caption">({{ performanceData.libres_count }} notas)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-4">
            <p>Total de notas evaluadas: {{ performanceData.total_notas_evaluadas }}</p>
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

  // Función para cargar rendimiento usando el store con cache
  const loadPerformanceAverage = async careerId => {
    await adminDashboardStore.fetchPerformanceAverage(careerId)
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadPerformanceAverage(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar al template
  const performanceData = computed(() => adminDashboardStore.careerPerformanceAverage || {
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
  const loading = computed(() => adminDashboardStore.isLoadingPerformanceAverage)
  const error = computed(() => adminDashboardStore.performanceAverageError)
</script>

<style scoped>
/* Asegurar distribución uniforme de las columnas */
.v-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

/* Asegurar que el círculo esté centrado dentro de cada columna */
.v-col > div:first-child {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>
