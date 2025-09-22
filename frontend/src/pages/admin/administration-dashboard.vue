<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="7" sm="10">
        <v-row class="mt-4" justify="center">
          <v-col cols="12" md="7" sm="10">
            <CareerAutocomplete
              v-model="selectedCareerId"
              label="Seleccionar Carrera"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <h3 class="text-center my-4">Inscripciones en Exámenes</h3>
            <CareerRegistrationsPanel :career-id="selectedCareerId" />
          </v-col>
          <v-col cols="12">
            <h3 class="text-center my-4">Rendimiento Académico</h3>
            <CareerPerformancePanel
              :error="error"
              :loading="loading"
              :performance-data="rendimientoGlobal"
            />
          </v-col>
          <v-col class="mb-8" cols="12">
            <h3 class="text-center my-4">Predicción de Rendimiento Académico</h3>
            <CareerPredictionPanel :career-id="selectedCareerId" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { watch } from 'vue'
  import CareerAutocomplete from '@/components/autocomplete/CareerAutocomplete.vue'
  import CareerPerformancePanel from '@/components/dashboard/CareerPerformancePanel.vue'
  import CareerPredictionPanel from '@/components/dashboard/CareerPredictionPanel.vue'
  import CareerRegistrationsPanel from '@/components/dashboard/CareerRegistrationsPanel.vue'
  import { useAdminDashboardStore } from '@/stores/adminDashboard'

  // Inicializar el store de dashboard admin
  const adminDashboardStore = useAdminDashboardStore()

  // Estado reactivo para almacenar el ID de la carrera seleccionada
  const selectedCareerId = ref(null)

  // Cargar rendimiento global usando el store con cache
  const loadRendimiento = async careerId => {
    await adminDashboardStore.fetchGlobalPerformance(careerId)
  }

  // Observa cambios en el ID de la carrera seleccionada
  watch(selectedCareerId, newId => {
    if (newId) {
      loadRendimiento(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar a componentes
  const rendimientoGlobal = computed(() => adminDashboardStore.globalPerformance || {
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
  const loading = computed(() => adminDashboardStore.isLoadingGlobalPerformance)
  const error = computed(() => adminDashboardStore.globalPerformanceError)
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
