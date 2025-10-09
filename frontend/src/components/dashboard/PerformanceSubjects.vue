<template>
  <v-card>
    <!-- Botón - Maximizar (solo cuando hay datos) -->
    <div v-if="hasData" style="position: absolute; top: 8px; right: 8px; z-index: 1;">
      <v-btn
        icon
        small
        title="Fullscreen"
        @click="showFullscreenDialog = true"
      >
        <v-icon>mdi-fullscreen</v-icon>
      </v-btn>
    </div>

    <!-- Vista - Normal -->
    <v-card-text class="pa-2 px-4">
      <div v-if="loading" class="text-center">
        <v-progress-circular indeterminate />
        <p>Cargando gráfico de barras...</p>
      </div>
      <div v-else-if="error" class="text-center">
        <p>{{ error }}</p>
      </div>
      <div v-else>
        <div class="chart-container">
          <apexchart
            :key="`chart-normal-${chartData.carrera_id}-${chartData.materias.length}`"
            height="400"
            :options="chartOptions"
            :series="chartSeries"
            type="bar"
            width="100%"
          />
        </div>
      </div>
    </v-card-text>
  </v-card>

  <!-- Vista - Pantalla completa -->
  <v-dialog
    v-model="showFullscreenDialog"
    fullscreen
  >
    <v-card>
      <v-card-title class="d-flex justify-end pa-5">
        <v-btn
          icon
          title="Cerrar"
          @click="showFullscreenDialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <div class="chart-container-fullscreen">
          <apexchart
            :key="`chart-fullscreen-${chartData.carrera_id}-${chartData.materias.length}-${showFullscreenDialog}`"
            height="800"
            :options="chartOptionsFullscreen"
            :series="chartSeries"
            type="bar"
            width="100%"
          />
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { useAdminDashboardStore } from '@/stores/adminDashboard'

  // Props
  const props = defineProps({
    careerId: {
      type: Number,
      required: false,
    },
  })

  // Composable
  const adminDashboardStore = useAdminDashboardStore()

  // Estado reactivo para controlar el modal de pantalla completa
  const showFullscreenDialog = ref(false)

  // Datos "fantasma" para mostrar cuando no hay datos reales
  const ghostSubjects = [
    { materia_nombre: 'Materia A', materia_promedio: 5 },
    { materia_nombre: 'Materia B', materia_promedio: 5 },
    { materia_nombre: 'Materia C', materia_promedio: 5 },
    { materia_nombre: 'Materia D', materia_promedio: 5 },
    { materia_nombre: 'Materia E', materia_promedio: 5 },
    { materia_nombre: 'Materia F', materia_promedio: 5 },
    { materia_nombre: 'Materia G', materia_promedio: 5 },
    { materia_nombre: 'Materia H', materia_promedio: 5 },
    { materia_nombre: 'Materia I', materia_promedio: 5 },
    { materia_nombre: 'Materia J', materia_promedio: 5 },
  ]

  // Reactive computeds
  const chartData = computed(() => {
    const realData = adminDashboardStore.careerPerformanceSubjects
    if (!realData || !realData.materias || realData.materias.length === 0) {
      return {
        carrera_id: null,
        carrera_nombre: 'Selecciona una carrera',
        materias: ghostSubjects,
      }
    }
    return realData
  })

  const loading = computed(() => adminDashboardStore.isLoadingPerformanceSubjects)
  const error = computed(() => adminDashboardStore.performanceSubjectsError)
  const hasData = computed(() => chartData.value.materias && chartData.value.materias.length > 0)

  // Computed para verificar si los datos actuales son los "fantasma"
  const isGhostData = computed(() => chartData.value.materias === ghostSubjects)

  // Chart options para el gráfico normal (sin etiquetas del eje X)
  const chartOptions = computed(() => ({
    // GRÁFICO
    chart: {
      type: 'bar', // Tipo de barras verticales
      height: 360, // Altura del gráfico
      toolbar: {
        show: false, // Ocultar menú de descarga en vista normal
      },
      // ANIMACIONES
      animations: {
        enabled: true,
        easing: 'easeinout', // Tipo de animación suave
        speed: 1000, // Velocidad de animación (1 segundo)
        animateGradually: {
          enabled: true,
          delay: 150, // Retraso entre barras
        },
        dynamicAnimation: {
          enabled: true,
          speed: 350, // Animación dinámica más rápida
        },
      },
    },
    // CUADRÍCULA
    grid: {
      padding: {
        left: 20,
        right: 20,
        bottom: 0,
        top: 20,
      },
      show: false, // Cuadrícula oculta para mejor apariencia
    },

    // BARRAS
    plotOptions: {
      bar: {
        horizontal: false, // Barras verticales
        columnWidth: '85%', // Ancho de las barras
        barHeight: '85%', // Altura de las barras
        endingShape: 'rounded', // Parte superior redondeada
        borderRadius: 4, // Bordes redondeados
        distributed: true, // Separa las barras uniformemente
      },
    },

    // ETIQUETAS: Deshabilitadas para evitar clutter
    dataLabels: {
      enabled: false,
    },

    // PALETA DE COLORES: Color único por barra
    colors: isGhostData.value
      ? ['#607D8B'] // Un color gris para las barras fantasma
      : [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
        '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
      ],

    // LEYENDA: Oculta, cada barra representa una materia individual
    legend: {
      show: false,
    },
    // Eje X sin etiquetas para modo normal
    xaxis: {
      categories: chartData.value.materias.map(m => m.materia_nombre),
      labels: {
        show: false, // Ocultar etiquetas en modo normal
      },
      title: {
        text: 'Materias',
        style: {
          color: '#ffffff',
          fontWeight: 'normal',
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: '#ffffff',
        },
      },
      title: {
        text: 'Promedio',
        style: {
          color: '#ffffff',
          fontWeight: 'normal',
        },
      },
      max: 10,
      min: 0,
      tickAmount: 10,
    },
    tooltip: {
      theme: 'dark',
      fillSeriesColor: false,
      style: {
        color: '#ffffff',
      },
      y: {
        formatter: function (val, { dataPointIndex }) {
          const materiaNombre = chartData.value.materias[dataPointIndex]?.materia_nombre || 'N/A'
          return `${materiaNombre}: ${val.toFixed(1)}`
        },
      },
    },
    responsive: [
      {
        breakpoint: 770,
        options: {
          chart: {
            height: 300,
          },
          plotOptions: {
            bar: {
              columnWidth: '70%',
              distributed: true,
            },
          },
          xaxis: {
            labels: {
              show: false, // Mantener ocultas en responsive
            },
          },
        },
      },
      {
        breakpoint: 480,
        options: {
          chart: {
            height: 220,
          },
          plotOptions: {
            bar: {
              columnWidth: '60%',
              distributed: true,
            },
          },
          xaxis: {
            labels: {
              show: false, // Mantener ocultas en responsive
            },
          },
        },
      },
    ],
  }))

  // Chart options para pantalla completa (con etiquetas del eje X)
  const chartOptionsFullscreen = computed(() => ({
    // GRÁFICO
    chart: {
      type: 'bar', // Tipo de barras verticales
      height: 900, // Altura del gráfico
      // ANIMACIONES
      animations: {
        enabled: true,
        easing: 'easeinout', // Tipo de animación suave
        speed: 1000, // Velocidad de animación (1 segundo)
        animateGradually: {
          enabled: true,
          delay: 150, // Retraso entre barras
        },
        dynamicAnimation: {
          enabled: true,
          speed: 350, // Animación dinámica más rápida
        },
      },
    },
    // CUADRÍCULA
    grid: {
      padding: {
        left: 20,
        right: 20,
        bottom: 70,
        top: 20,
      },
      show: false, // Cuadrícula oculta para mejor apariencia
    },

    // BARRAS
    plotOptions: {
      bar: {
        horizontal: false, // Barras verticales
        columnWidth: '85%', // Ancho de las barras
        barHeight: '85%', // Altura de las barras
        endingShape: 'rounded', // Parte superior redondeada
        borderRadius: 4, // Bordes redondeados
        distributed: true, // Separa las barras uniformemente
      },
    },

    // ETIQUETAS: Deshabilitadas para evitar clutter
    dataLabels: {
      enabled: false,
    },

    // PALETA DE COLORES: Color único por barra
    colors: isGhostData.value
      ? ['#607D8B'] // Un color gris para las barras fantasma
      : [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
        '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
      ],

    // LEYENDA: Oculta, cada barra representa una materia individual
    legend: {
      show: false,
    },
    // Eje X con etiquetas para pantalla completa
    xaxis: {
      categories: chartData.value.materias.map(m => m.materia_nombre),
      labels: {
        rotate: -40,
        style: {
          colors: '#ffffff',
          fontSize: '9px',
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: '#ffffff',
        },
      },
      title: {
        text: 'Promedio',
        style: {
          color: '#ffffff',
          fontWeight: 'normal',
        },
      },
      max: 10,
      min: 0,
      tickAmount: 10,
    },
    tooltip: {
      theme: 'dark',
      fillSeriesColor: false,
      style: {
        color: '#ffffff',
      },
      y: {
        formatter: function (val, { dataPointIndex }) {
          const materiaNombre = chartData.value.materias[dataPointIndex]?.materia_nombre || 'N/A'
          return `${materiaNombre}: ${val.toFixed(1)}`
        },
      },
    },
    responsive: [
      {
        breakpoint: 1200,
        options: {
          chart: {
            height: 600,
          },
          xaxis: {
            labels: {
              rotate: -40,
              style: {
                fontSize: '9px',
              },
            },
          },
        },
      },
      {
        breakpoint: 770,
        options: {
          chart: {
            height: 500,
          },
          xaxis: {
            labels: {
              rotate: -40,
              style: {
                fontSize: '9px',
              },
            },
          },
        },
      },
    ],
  }))

  // Chart series data - Una sola serie con colores por posición
  const chartSeries = computed(() => [
    {
      name: 'Promedio',
      data: chartData.value.materias.map(materia => materia.materia_promedio || 0),
    },
  ])

  // Watch para cambios en careerId
  watch(() => props.careerId, newId => {
    if (newId) {
      adminDashboardStore.fetchPerformanceSubjects(newId)
    }
  }, { immediate: true })

  // Watch para cambios en los datos del gráfico
  watch(() => chartData.value.materias, () => {
    // Watcher para detectar cambios en los datos del gráfico
  }, { deep: true, immediate: true })

  // Watch para el modal de pantalla completa
  watch(() => showFullscreenDialog.value, newValue => {
    if (newValue && hasData.value) {
      // El modal se maneja automáticamente con la key del componente
    }
  })
</script>

<style scoped>
/* Estilos para el contenedor del gráfico */
.chart-container {
  width: 100%;
  overflow: hidden;
}

.chart-container-fullscreen {
  width: 100%;
  overflow: hidden;
}
</style>
