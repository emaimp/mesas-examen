<template>
  <v-col cols="12">
    <v-card>
      <v-card-text>
        <v-row>
          <v-col cols="6">
            <p>Nombre: {{ digitalAct.estudiante_nombre }}</p>
            <p>DNI: {{ digitalAct.dni }}</p>
            <p>Libreta: {{ digitalAct.libreta }}</p>
            <p>Nota: {{ digitalAct.nota }}</p>
          </v-col>
          <v-col cols="6">
            <p>Inscripcion: {{ capitalizeFirstLetter(digitalAct.tipo_inscripcion) }}</p>
            <p>Llamado: {{ formattedLlamado }}</p>
            <p>Fecha: {{ new Date(digitalAct.fecha_llamado).toLocaleDateString() }}</p>
            <p>Asistencia: {{ capitalizeFirstLetter(digitalAct.asistencia) }}</p>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    digitalAct: {
      type: Object,
      required: true,
    },
  })

  const capitalizeFirstLetter = string => {
    if (!string) return ''
    return string.charAt(0).toUpperCase() + string.slice(1)
  }

  const formattedLlamado = computed(() => {
    const llamadoMap = {
      primer_llamado: 'Primer llamado',
      segundo_llamado: 'Segundo llamado',
      tercer_llamado: 'Tercer llamado',
    }
    return llamadoMap[props.digitalAct.llamado_inscrito] || props.digitalAct.llamado_inscrito
  })
</script>

<style scoped>
.v-card {
  box-shadow: none !important;
  background: #ffffff !important;
  border: 1px solid #000000 !important;
}

.v-card-text p {
  color: #000000 !important;
}
</style>
