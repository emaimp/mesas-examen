<template>
  <v-card class="pa-6">
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

              <!-- Muestra los datos por defecto (0%) -->
              <div v-if="isDefaultData" class="mt-4">
                <v-row justify="center">
                  <v-col class="text-center" xs="12" sm="6" md="4">
                    <PercentageCircle
                      color="green_color"
                      :value="0"
                    />
                    <p class="mt-2 text-caption">Promocionados</p>
                    <p class="mt-0 text-caption">(0)</p>
                  </v-col>
                  <v-col class="text-center" xs="12" sm="6" md="4">
                    <PercentageCircle
                      color="yellow_color"
                      :value="0"
                    />
                    <p class="mt-2 text-caption">Regulares</p>
                    <p class="mt-0 text-caption">(0)</p>
                  </v-col>
                  <v-col class="text-center" xs="12" sm="6" md="4">
                    <PercentageCircle
                      color="red_color"
                      :value="0"
                    />
                    <p class="mt-2 text-caption">Libres</p>
                    <p class="mt-0 text-caption">(0)</p>
                  </v-col>
                </v-row>
                <div class="text-center mt-4">
                  <p>Total: 0</p>
                </div>
              </div>

              <!-- Muestra los datos cuando se seleccioná una carrera -->
              <div v-else>
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
                    <v-card variant="outlined" class="pa-6">
                      <h4 class="text-subtitle-1 mb-2">{{ subKey }}</h4>
                      <v-row justify="space-around" class="flex-wrap">
                        <div class="text-center px-3">
                          <PercentageCircle
                            color="green_color"
                            :value="subData.promocionado_pct"
                          />
                          <p class="mt-1 text-caption">Promocionados</p>
                          <p class="mt-0 text-caption">({{ subData.promocionado }})</p>
                        </div>
                        <div class="text-center px-3">
                          <PercentageCircle
                            color="yellow_color"
                            :value="subData.regular_pct"
                          />
                          <p class="mt-1 text-caption">Regulares</p>
                          <p class="mt-0 text-caption">({{ subData.regular }})</p>
                        </div>
                        <div class="text-center px-3">
                          <PercentageCircle
                            color="red_color"
                            :value="subData.libre_pct"
                          />
                          <p class="mt-1 text-caption">Libres</p>
                          <p class="mt-0 text-caption">({{ subData.libre }})</p>
                        </div>
                      </v-row>
                      <p class="mt-6 text-caption">Total: {{ subData.total }}</p>
                    </v-card>
                  </v-col>
                </v-row>
              </div>

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

  // Datos predeterminados para mostrar cuando no hay datos cargados
  const defaultDemograficos = {
    genero: {
      'Sin datos': {
        promocionado_pct: 0,
        regular_pct: 0,
        libre_pct: 0,
        promocionado: 0,
        regular: 0,
        libre: 0,
        total: 0,
      },
    },
    edad: {
      'Sin datos': {
        promocionado_pct: 0,
        regular_pct: 0,
        libre_pct: 0,
        promocionado: 0,
        regular: 0,
        libre: 0,
        total: 0,
      },
    },
    localidad: {
      'Sin datos': {
        promocionado_pct: 0,
        regular_pct: 0,
        libre_pct: 0,
        promocionado: 0,
        regular: 0,
        libre: 0,
        total: 0,
      },
    },
    ocupacion: {
      'Sin datos': {
        promocionado_pct: 0,
        regular_pct: 0,
        libre_pct: 0,
        promocionado: 0,
        regular: 0,
        libre: 0,
        total: 0,
      },
    },
  }

  // Reactive computeds para pasar al template
  const demographicData = computed(() => adminDashboardStore.careerPerformanceDemographic?.demograficos || defaultDemograficos)
  const loading = computed(() => adminDashboardStore.isLoadingPerformanceDemographic)
  const error = computed(() => adminDashboardStore.performanceDemographicError)

  // Computed para verificar si solo hay datos por defecto ('Sin datos')
  const isDefaultData = computed(() => {
    const currentData = demographicData.value[activeTab.value]
    return currentData && Object.keys(currentData).length === 1 && Object.keys(currentData)[0] === 'Sin datos'
  })

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
/* Estilos para el v-card */
.v-card {
  box-shadow: none !important; /* Tarjeta sin sombra */
}
</style>
