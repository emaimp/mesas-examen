<template>
  <div class="text-center">
    <v-progress-circular
      :color="color"
      :model-value="animatedValue"
      :rotate="360"
      :size="circleSize"
      :width="15"
    >
      <template #default> {{ animatedValue }} % </template>
    </v-progress-circular>
  </div>
</template>

<script setup>
  import { useDisplay } from 'vuetify'

  // Define las propiedades que este componente puede recibir
  const props = defineProps({
    value: { // El valor numérico que representa el porcentaje
      type: Number,
      required: false,
      default: 0,
    },
    color: { // El color del círculo de progreso
      type: String,
      default: 'teal',
    },
  })

  // Obtiene el objeto de display de Vuetify para acceder a los breakpoints
  const display = useDisplay()

  // Propiedad computada para determinar el tamaño del círculo basado en el tamaño de la pantalla
  const circleSize = computed(() => {
    if (display.xs.value) {
      return 60 // Para pantallas muy pequeñas
    } else if (display.smAndDown.value) {
      return 80 // Para sm
    } else if (display.mdAndUp.value) {
      return 100 // Para md y lg
    } else {
      return 120 // Para xl muy grandes
    }
  })

  // Estado reactivo para el valor animado del porcentaje
  const animatedValue = ref(0)
  // ID para controlar la animación de requestAnimationFrame
  let animationFrameId = null

  /**
   * Anima el valor del porcentaje de un inicio a un fin durante una duración
   * @param {number} start - Valor inicial de la animación
   * @param {number} end - Valor final de la animación
   * @param {number} duration - Duración de la animación en milisegundos
   */
  const animateValue = (start, end, duration) => {
    let startTime = null

    // Función que se ejecuta en cada fotograma de la animación
    const step = currentTime => {
      if (!startTime) startTime = currentTime
      // Calcula el progreso de la animación (0 a 1)
      const progress = Math.min((currentTime - startTime) / duration, 1)
      // Actualiza el valor animado, redondeando hacia abajo
      animatedValue.value = Math.floor(start + (end - start) * progress)

      // Si la animación no ha terminado, solicita el siguiente fotograma
      if (progress < 1) {
        animationFrameId = requestAnimationFrame(step)
      }
    }

    // Inicia la animación
    animationFrameId = requestAnimationFrame(step)
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(() => {
    // Inicia la animación del valor desde 0 hasta el valor de la prop
    animateValue(0, props.value, 1000)
  })

  // Observa cambios en la prop 'value'
  watch(() => props.value, newValue => {
    // Si hay una animación en curso, la cancela
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId)
    }
    // Inicia una nueva animación desde el valor actual hasta el nuevo valor
    animateValue(animatedValue.value, newValue, 1000)
  }, { immediate: true }) // Ejecuta el watcher inmediatamente al montar el componente
</script>

<style scoped>
/* Estilos para el círculo de progreso */
.v-progress-circular {
  margin: 0rem 1rem 1rem 1rem; /* Margin reducido arriba, mismo en lados e inferior */
}
</style>
