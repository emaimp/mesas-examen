<template>
  <v-card class="pa-4">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando aprobación de exámenes...</p>
        </div>
        <div v-else-if="error" class="text-center text-red">
          <p>{{ error }}</p>
        </div>
        <div v-else>
          <v-row class="my-0" justify="space-around">
            <v-col class="text-center" cols="12" sm="6">
              <PercentageCircle
                color="green_color"
                :value="approvedData.aprobados_percentage"
              />
              <p class="mt-2">Aprobados</p>
              <p class="mt-1">({{ approvedData.aprobados_count }} exámenes)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="6">
              <PercentageCircle
                color="red_color"
                :value="approvedData.desaprobados_percentage"
              />
              <p class="mt-2">Desaprobados</p>
              <p class="mt-1">({{ approvedData.desaprobados_count }} exámenes)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-5">
            <p><strong>Total de exámenes evaluados: {{ approvedData.total_examenes_evaluados }}</strong></p>
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
  const loadApproved = async careerId => {
    await adminDashboardStore.fetchGlobalApproved(careerId)
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadApproved(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar al template
  const approvedData = computed(() => adminDashboardStore.globalApproved || {
    carrera_id: null,
    carrera_nombre: 'Selecciona una carrera',
    aprobados_count: 0,
    aprobados_percentage: 0,
    desaprobados_count: 0,
    desaprobados_percentage: 0,
    total_examenes_evaluados: 0,
  })
  const loading = computed(() => adminDashboardStore.isLoadingApproved)
  const error = computed(() => adminDashboardStore.approvedError)
</script>

<style scoped>

</style>
