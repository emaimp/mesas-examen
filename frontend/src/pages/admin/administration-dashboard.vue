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
        <!-- Primera fila: Inscripciones y Aprobados -->
        <v-row class="mb-4">
          <v-col cols="12" md="6">
            <h3 class="text-center my-4">Inscripciones en Exámenes</h3>
            <CareerRegistrationsPanel :career-id="selectedCareerId" />
          </v-col>
          <v-col cols="12" md="6">
            <h3 class="text-center my-4">Aprobados en Exámenes</h3>
            <CareerApprovedPanel :career-id="selectedCareerId" />
          </v-col>
        </v-row>

        <!-- Segunda fila: Rendimiento y Predicción -->
        <v-row class="mb-8">
          <v-col cols="12" md="6">
            <h3 class="text-center my-4">Rendimiento Académico</h3>
            <CareerPerformancePanel :career-id="selectedCareerId" />
          </v-col>
          <v-col cols="12" md="6">
            <h3 class="text-center my-4">Predicción de Rendimiento Académico</h3>
            <CareerPredictionPanel :career-id="selectedCareerId" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import CareerAutocomplete from '@/components/autocomplete/CareerAutocomplete.vue'
  import CareerApprovedPanel from '@/components/dashboard/CareerApprovedPanel.vue'
  import CareerPerformancePanel from '@/components/dashboard/CareerPerformancePanel.vue'
  import CareerPredictionPanel from '@/components/dashboard/CareerPredictionPanel.vue'
  import CareerRegistrationsPanel from '@/components/dashboard/CareerRegistrationPanel.vue'
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
