<template>
  <v-card class="pa-5">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando inscripciones...</p>
        </div>
        <div v-else-if="error" class="text-center">
          <p>{{ error }}</p>
        </div>
        <div v-else>
          <v-row justify="center">
            <v-col class="text-center" xs="12" sm="6">
              <PercentageCircle
                color="green_color"
                :value="registrationsData.activos_percentage"
              />
              <p class="mt-2 text-caption">Activas</p>
              <p class="mt-0 text-caption">({{ registrationsData.activos_count }} inscripciones)</p>
            </v-col>
            <v-col class="text-center" xs="12" sm="6">
              <PercentageCircle
                color="red_color"
                :value="registrationsData.cancelados_percentage"
              />
              <p class="mt-2 text-caption">Canceladas</p>
              <p class="mt-0 text-caption">({{ registrationsData.cancelados_count }} inscripciones)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-4">
            <p>Total de inscripciones: {{ registrationsData.total_inscripciones }}</p>
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

  // Función para cargar registros usando el store con cache
  const loadPercentageRegistration = async careerId => {
    await adminDashboardStore.fetchPercentageRegistration(careerId)
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadPercentageRegistration(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar al template
  const registrationsData = computed(() => adminDashboardStore.careerPercentageRegistration || {
    carrera_id: null,
    carrera_nombre: 'Selecciona una carrera',
    activos_count: 0,
    activos_percentage: 0,
    cancelados_count: 0,
    cancelados_percentage: 0,
    total_inscripciones: 0,
  })
  const loading = computed(() => adminDashboardStore.isLoadingPercentageRegistration)
  const error = computed(() => adminDashboardStore.percentageRegistrationError)
</script>

<style scoped>
/* Estilos para el v-card */
.v-card {
  box-shadow: none !important; /* Tarjeta sin sombra */
}

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
