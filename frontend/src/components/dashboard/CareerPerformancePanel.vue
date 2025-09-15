<template>
  <v-card class="pa-4">
    <v-card-text>
      <v-row justify="center">
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate />
          <p>Cargando rendimiento...</p>
        </div>
        <div v-else-if="error" class="text-center text-red">
          <p>{{ error }}</p>
        </div>
        <div v-else-if="!performanceData || performanceData.total_notas_evaluadas === 0" class="text-center">
          <p>No hay datos de rendimiento disponibles.</p>
        </div>
        <div v-else>
          <v-row class="my-0" justify="space-around">
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="green_color"
                :value="performanceData.promocionados_percentage"
              />
              <p class="mt-2">Promocionados ({{ performanceData.promocionados_count }} notas)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="yellow_color"
                :value="performanceData.regulares_percentage"
              />
              <p class="mt-2">Regulares ({{ performanceData.regulares_count }} notas)</p>
            </v-col>
            <v-col class="text-center" cols="12" sm="4">
              <PercentageCircle
                color="red_color"
                :value="performanceData.libres_percentage"
              />
              <p class="mt-2">Libres ({{ performanceData.libres_count }} notas)</p>
            </v-col>
          </v-row>
          <div class="text-center mt-6">
            <p><strong>Total de notas evaluadas: {{ performanceData.total_notas_evaluadas }}</strong></p>
          </div>
        </div>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
  import PercentageCircle from './PercentageCircle.vue'

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const props = defineProps({
    performanceData: {
      type: Object,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    error: {
      type: String,
      required: false,
    },
  })
</script>

<style scoped>

</style>
