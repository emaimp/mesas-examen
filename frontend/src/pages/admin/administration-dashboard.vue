<template>
  <v-container>
    <v-row justify="center">
      <v-col md="8">
        <v-card class="pa-10 my-6">
          <v-row class="mt-0" justify="center">
            <v-col cols="12" md="8">
              <CareerAutocomplete
                v-model="selectedCareerId"
                label="Seleccioná una Carrera"
              />
            </v-col>
          </v-row>
          <!-- Primera fila: Inscripciones y Aprobados -->
          <v-row>
            <v-col>
              <h3 class="text-center my-6">Inscripciones en Exámenes</h3>
              <CareerRegistrationsPanel :career-id="selectedCareerId" />
            </v-col>
            <v-col>
              <h3 class="text-center my-6">Aprobados en Exámenes</h3>
              <CareerApprovedPanel :career-id="selectedCareerId" />
            </v-col>
          </v-row>

          <!-- Segunda fila: Rendimiento y Predicción -->
          <v-row>
            <v-col>
              <h3 class="text-center my-3">Rendimiento Académico</h3>
              <CareerPerformancePanel :career-id="selectedCareerId" />
            </v-col>
            <v-col>
              <h3 class="text-center my-3">Predicción de Rendimiento</h3>
              <CareerPredictionPanel :career-id="selectedCareerId" />
            </v-col>
          </v-row>

          <!-- Tercera fila: Rendimiento Demográfico -->
          <v-row>
            <v-col>
              <h3 class="text-center my-3">Rendimiento Demográfico</h3>
              <PerformanceDemographic :career-id="selectedCareerId" />
            </v-col>
          </v-row>

          <!-- Cuarta fila: Gráfico de Barras -->
          <v-row>
            <v-col class="mb-3">
              <h3 class="text-center my-3">Promedio por Materia</h3>
              <CareerBarChartPanel :career-id="selectedCareerId" />
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import CareerAutocomplete from '@/components/autocomplete/CareerAutocomplete.vue'
  import CareerRegistrationsPanel from '@/components/dashboard/PercentageRegistration.vue'
  import CareerPerformancePanel from '@/components/dashboard/PerformanceAverage.vue'
  import PerformanceDemographic from '@/components/dashboard/PerformanceDemographic.vue'
  import CareerPredictionPanel from '@/components/dashboard/PerformancePrediction.vue'
  import CareerBarChartPanel from '@/components/dashboard/PerformanceSubjects.vue'
  import CareerApprovedPanel from '@/components/dashboard/PerformanceTableExam.vue'
  import { useAdminDashboardStore } from '@/stores/adminDashboard'

  // Inicializar el store de dashboard admin
  const adminDashboardStore = useAdminDashboardStore()

  // Estado reactivo para almacenar el ID de la carrera seleccionada
  const selectedCareerId = ref(null)

  // Resetear estado al activar la página (volver de otra pestaña)
  onActivated(() => {
    adminDashboardStore.resetAll()
    selectedCareerId.value = null
  })
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
