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
