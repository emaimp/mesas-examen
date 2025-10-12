<template>
  <v-col cols="12" sm="6">
    <v-card
      class="clickable"
      :flat="true"
      @click="emit('open-registered-dialog', estudiante)"
    >
      <v-card-title class="text-wrap text-subtitle-1 pb-1">
        {{ estudiante.materia_nombre }}
      </v-card-title>
      <v-card-subtitle class="pt-0 pb-2">
        Tipo de Inscripción: {{ formatTipoInscripcion(estudiante.tipo_inscripcion) }}
      </v-card-subtitle>
      <v-card-subtitle class="pt-0 pb-2">
        {{ estudiante.llamado_inscrito === 'primer_llamado' ? 'Primer Llamado' : 'Segundo Llamado' }}: {{ formatFechaHora(estudiante.fecha_llamado) }}
      </v-card-subtitle>
      <v-card-text class="pt-2 pb-2">
        Estudiante: {{ estudiante.nombre_estudiante }}<br>
        DNI: {{ estudiante.dni }}<br>
        Libreta: {{ estudiante.libreta }}<br>
        Carrera: {{ estudiante.carrera_nombre }}
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script setup>
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const props = defineProps({
    // Define la propiedad 'estudiante' que es un objeto y es requerida
    estudiante: {
      type: Object,
      required: true,
      // Validador para asegurar que el objeto 'estudiante' tenga las propiedades necesarias
      validator: value => {
        return value && value.estudiante_nombre && value.dni && value.libreta && value.carrera_nombre && value.materia_nombre && value.fecha_llamado && value.llamado_inscrito && value.tipo_inscripcion
      },
    },
  })

  // Define los eventos que este componente puede emitir
  const emit = defineEmits(['open-registered-dialog'])

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

  /**
   * Formatea el tipo de inscripción para mostrar la primera letra en mayúscula
   * @param {string} tipo - El tipo de inscripción (ej. "libre", "regular")
   * @returns {string} El tipo de inscripción formateado (ej. "Libre", "Regular")
   */
  const formatTipoInscripcion = tipo => {
    if (!tipo) return ''
    return tipo.charAt(0).toUpperCase() + tipo.slice(1)
  }
</script>

<style scoped>
/* Estilos para la tarjeta del estudiante registrado */
.v-card {
  margin-bottom: 16px; /* Margen inferior para separar las tarjetas */
  box-shadow: none !important; /* Tarjeta sin sombra */
  background: linear-gradient(to right bottom, #001f54, #34a0a4) !important;
}
</style>
