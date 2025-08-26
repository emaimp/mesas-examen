<template>
  <v-col cols="12" sm="6">
    <v-card
      :class="['mesa-card', 'clickable', cardClass]"
      :flat="true"
      @click="emit('open-registered-dialog', mesa)"
    >
      <v-card-title class="text-wrap text-subtitle-1 pb-1">
        {{ mesa.materia_nombre }}
      </v-card-title>
      <v-card-subtitle class="pt-0 pb-2">
        {{ formatFechaHora(mesa.fecha) }}
      </v-card-subtitle>
      <v-card-text class="pt-0 pb-2">
        Profesor: {{ mesa.profesor_nombre }}
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script setup>
  const props = defineProps({
    // Define la propiedad 'mesa' que es un objeto y es requerida
    mesa: {
      type: Object,
      required: true,
      // Validador para asegurar que el objeto 'mesa' tenga las propiedades necesarias
      validator: value => {
        return value && value.id && value.materia_nombre && value.fecha && value.profesor_nombre && value.estado
      },
    },
  })

  // Define los eventos que este componente puede emitir
  const emit = defineEmits(['open-registered-dialog'])

  // Propiedad computada para determinar la clase CSS de la tarjeta según el estado de la inscripción
  const cardClass = computed(() => {
    if (props.mesa && props.mesa.estado === 'canceled') {
      return 'mesa-card-canceled' // Clase para inscripciones canceladas
    }
    return 'mesa-card-active' // Clase para inscripciones activas
  })

  /**
   * Formatea una cadena de fecha ISO a un formato legible en español
   * @param {string} isoString - La cadena de fecha en formato ISO
   * @returns {string} La fecha y hora formateada o 'Fecha no disponible'
   */
  const formatFechaHora = isoString => {
    if (!isoString) return 'Fecha no disponible'
    const date = new Date(isoString)
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }
    return date.toLocaleDateString('es-ES', options)
  }
</script>

<style scoped>
/* Estilos para la tarjeta de la mesa de examen */
.mesa-card {
  margin-bottom: 16px; /* Margen inferior para separar las tarjetas */
}

/* Estilos para tarjetas de inscripción activa */
.v-card.mesa-card.mesa-card-active {
  background: linear-gradient(to right, #0d730d, #008000) !important;
}

/* Estilos para tarjetas de inscripción cancelada */
.v-card.mesa-card.mesa-card-canceled {
  background: linear-gradient(to right, #a82424, #cd0000) !important;
}
</style>
