<template>
  <v-card class="pa-5">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando aprobación de exámenes...</p>
        </div>
        <div v-else-if="error" class="text-center">
          <p>{{ error }}</p>
        </div>
        <div v-else>
          <v-row justify="center">
            <v-col class="text-center" xs="12" sm="6">
              <PercentageCircle
                color="green_color"
                :value="approvedData.aprobados_percentage"
              />
              <p class="mt-2 text-caption">Aprobados</p>
              <p class="mt-0 text-caption">({{ approvedData.aprobados_count }} exámenes)</p>
            </v-col>
            <v-col class="text-center" xs="12" sm="6">
              <PercentageCircle
                color="red_color"
                :value="approvedData.desaprobados_percentage"
              />
              <p class="mt-2 text-caption">Desaprobados</p>
              <p class="mt-0 text-caption">({{ approvedData.desaprobados_count }} exámenes)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-4">
            <p>Total de exámenes evaluados: {{ approvedData.total_examenes_evaluados }}</p>
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

  // Función para cargar aprobación usando el store con cache
  const loadPerformanceTableExam = async careerId => {
    await adminDashboardStore.fetchPerformanceTableExam(careerId)
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadPerformanceTableExam(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar al template
  const approvedData = computed(() => adminDashboardStore.careerPerformanceTableExam || {
    carrera_id: null,
    carrera_nombre: 'Selecciona una carrera',
    aprobados_count: 0,
    aprobados_percentage: 0,
    desaprobados_count: 0,
    desaprobados_percentage: 0,
    total_examenes_evaluados: 0,
  })
  const loading = computed(() => adminDashboardStore.isLoadingPerformanceTableExam)
  const error = computed(() => adminDashboardStore.performanceTableExamError)
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
