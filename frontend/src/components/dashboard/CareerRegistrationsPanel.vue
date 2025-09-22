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
  const loadRegistrations = async careerId => {
    await adminDashboardStore.fetchExamRegistrations(careerId)
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadRegistrations(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar al template
  const registrationsData = computed(() => adminDashboardStore.examRegistrations || {
    carrera_id: null,
    carrera_nombre: 'Selecciona una carrera',
    activos_count: 0,
    activos_percentage: 0,
    cancelados_count: 0,
    cancelados_percentage: 0,
    total_inscripciones: 0,
  })
  const loading = computed(() => adminDashboardStore.isLoadingRegistrations)
  const error = computed(() => adminDashboardStore.registrationsError)
</script>

<style scoped>

</style>
