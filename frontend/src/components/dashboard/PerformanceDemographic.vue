<template>
  <v-card class="pa-4">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando rendimiento demográfico...</p>
        </div>
        <div v-else-if="error" class="text-center">
          <p>{{ error }}</p>
        </div>
        <div v-else>
          <v-tabs v-model="activeTab" color="primary" grow>
            <v-tab v-for="demoType in Object.keys(demographicData)" :key="demoType" :value="demoType">
              {{ getTabLabel(demoType) }}
            </v-tab>
          </v-tabs>

          <v-tabs-window v-model="activeTab">
            <v-tabs-window-item v-for="demoType in Object.keys(demographicData)" :key="demoType" :value="demoType">
              <v-row justify="space-between" class="mt-4">
                <v-col
                  v-for="(subData, subKey) in demographicData[demoType]"
                  :key="subKey"
                  xs="12"
                  sm="6"
                  md="6"
                  lg="6"
                  class="text-center"
                >
                  <v-card variant="outlined" class="pa-9">
                    <h4 class="text-subtitle-1 mb-2">{{ subKey }}</h4>
                    <v-row justify="space-around" class="flex-wrap">
                      <div class="text-center">
                        <PercentageCircle
                          color="green_color"
                          :value="subData.promocionado_pct"
                        />
                        <p class="mt-1 text-caption">Promocionados</p>
                        <p class="mt-0 text-caption">({{ subData.promocionado }})</p>
                      </div>
                      <div class="text-center">
                        <PercentageCircle
                          color="yellow_color"
                          :value="subData.regular_pct"
                        />
                        <p class="mt-1 text-caption">Regulares</p>
                        <p class="mt-0 text-caption">({{ subData.regular }})</p>
                      </div>
                      <div class="text-center">
                        <PercentageCircle
                          color="red_color"
                          :value="subData.libre_pct"
                        />
                        <p class="mt-1 text-caption">Libres</p>
                        <p class="mt-0 text-caption">({{ subData.libre }})</p>
                      </div>
                    </v-row>
                    <p class="mt-3 text-caption">Total: {{ subData.total }}</p>
                  </v-card>
                </v-col>
              </v-row>
            </v-tabs-window-item>
          </v-tabs-window>
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

  // Estado reactivo para la tab activa
  const activeTab = ref('genero')

  // Función para cargar rendimiento demográfico usando el store
  const loadPerformanceDemographic = async careerId => {
    await adminDashboardStore.fetchPerformanceDemographic(careerId)
  }

  // Observa cambios en el ID de la carrera
  watch(() => props.careerId, newId => {
    if (newId) {
      loadPerformanceDemographic(newId)
    }
  }, { immediate: true })

  // Reactive computeds para pasar al template
  const demographicData = computed(() => adminDashboardStore.careerPerformanceDemographic?.demograficos || {})
  const loading = computed(() => adminDashboardStore.isLoadingPerformanceDemographic)
  const error = computed(() => adminDashboardStore.performanceDemographicError)

  // Función para obtener etiquetas legibles para las tabs
  const getTabLabel = demoType => {
    const labels = {
      genero: 'Género',
      edad: 'Edad',
      localidad: 'Localidad',
      ocupacion: 'Ocupación',
    }
    return labels[demoType] || demoType
  }
</script>

<style scoped>
/* No hay estilos personalizados necesarios por ahora */
</style>
