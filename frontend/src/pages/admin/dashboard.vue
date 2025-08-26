<template>
  <v-container>
    <v-row justify="center">
      <v-col class="d-flex align-center justify-center" cols="12" lg="6" md="6">
        <v-card class="pa-6 flex-grow-1">
          <v-card-title class="text-h5 my-7 text-center">
            Rendimiento de una Carrera
          </v-card-title>
          <v-card-text>
            <v-row justify="center">
              <v-col cols="12" md="10" sm="10">
                <CareerAutocomplete
                  v-model="selectedCareerId"
                  label="Seleccionar Carrera"
                />
              </v-col>
              <v-row class="my-7" justify="space-around">

                <div v-if="loading" class="text-center">
                  <v-progress-circular indeterminate />
                  <p>Cargando...</p>
                </div>
                <div v-else-if="error" class="text-center text-red">
                  <p>{{ error }}</p>
                </div>
                <div v-else-if="!selectedCareerId" class="text-center">
                  <p>Por favor, selecciona una carrera.</p>
                </div>
                <div v-else-if="rendimientoGlobal.total_notas_evaluadas === 0" class="text-center">
                  <p>No hay notas registradas.</p>
                </div>
                <div v-else>
                  <v-row class="my-0" justify="space-around">
                    <v-col class="text-center" cols="12" sm="4">
                      <PercentageCircle
                        color="green_color"
                        :value="rendimientoGlobal.promocionados_percentage"
                      />
                      <p class="mt-2">Promocionados ({{ rendimientoGlobal.promocionados_count }} notas)</p>
                    </v-col>
                    <v-col class="text-center" cols="12" sm="4">
                      <PercentageCircle
                        color="yellow_color"
                        :value="rendimientoGlobal.regulares_percentage"
                      />
                      <p class="mt-2">Regulares ({{ rendimientoGlobal.regulares_count }} notas)</p>
                    </v-col>
                    <v-col class="text-center" cols="12" sm="4">
                      <PercentageCircle
                        color="red_color"
                        :value="rendimientoGlobal.libres_percentage"
                      />
                      <p class="mt-2">Libres ({{ rendimientoGlobal.libres_count }} notas)</p>
                    </v-col>
                  </v-row>
                  <div class="text-center mt-10">
                    <p>Total de notas evaluadas: {{ rendimientoGlobal.total_notas_evaluadas }}</p>
                  </div>
                </div>
              </v-row></v-row></v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import CareerAutocomplete from '@/components/autocomplete/CareerAutocomplete.vue'
  import PercentageCircle from '@/components/dashboard/PercentageCircle.vue'
  import { useRendimientoGlobalCarrera } from '@/services/admin/useGlobalPerformance'

  // Inicializa el servicio para obtener el rendimiento global
  const { fetchGlobalPerformance } = useRendimientoGlobalCarrera()

  // Estado reactivo para almacenar los datos de rendimiento global
  const rendimientoGlobal = ref({
    carrera_id: null,
    carrera_nombre: 'Cargando...',
    promocionados_count: 0,
    promocionados_percentage: 0,
    regulares_count: 0,
    regulares_percentage: 0,
    libres_count: 0,
    libres_percentage: 0,
    total_notas_evaluadas: 0,
  })
  // Estado reactivo para indicar si los datos están cargando
  const loading = ref(false)
  // Estado reactivo para almacenar mensajes de error
  const error = ref(null)
  // Estado reactivo para almacenar el ID de la carrera seleccionada
  const selectedCareerId = ref(null)

  /**
   * Carga el rendimiento global de una carrera específica
   * @param {number} careerId - El ID de la carrera
   */
  const loadRendimiento = async careerId => {
    loading.value = true // Activa el estado de carga
    error.value = null // Limpia errores previos
    rendimientoGlobal.value.carrera_nombre = 'Cargando...' // Muestra estado de carga para el nombre de la carrera
    try {
      // Obtiene los datos de rendimiento de la API
      const data = await fetchGlobalPerformance(careerId)
      if (data) {
        rendimientoGlobal.value = data // Asigna los datos si la respuesta es exitosa
      } else {
        error.value = 'No se pudo cargar el rendimiento global de la carrera.'
        rendimientoGlobal.value.carrera_nombre = 'No encontrada'
      }
    } catch (error_) {
      error.value = error_.message || 'Ocurrió un error al cargar los datos.' // Captura y muestra errores
      rendimientoGlobal.value.carrera_nombre = 'Error'
    } finally {
      loading.value = false // Desactiva el estado de carga
    }
  }

  // Observa cambios en el ID de la carrera seleccionada
  watch(selectedCareerId, newId => {
    if (newId) {
      loadRendimiento(newId) // Si se selecciona una carrera, carga su rendimiento
    } else {
      // Si no hay carrera seleccionada, restablece los valores a cero
      rendimientoGlobal.value = {
        carrera_id: null,
        carrera_nombre: 'Selecciona una carrera',
        promocionados_count: 0,
        promocionados_percentage: 0,
        regulares_count: 0,
        regulares_percentage: 0,
        libres_count: 0,
        libres_percentage: 0,
        total_notas_evaluadas: 0,
      }
      loading.value = false
      error.value = null
    }
  }, { immediate: true }) // Ejecuta el watcher inmediatamente al montar el componente
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
