<template>
  <v-row>
    <v-col cols="6">
      <v-menu
        v-model="menu"
        activator="parent"
        :close-on-content-click="false"
        min-width="auto"
        offset-y
        transition="scale-transition"
      >
        <template #activator="{ props }">
          <v-text-field
            v-model="formattedDate"
            label="Fecha"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="props"
            style="width: 100%;"
          />
        </template>
        <v-date-picker
          v-model="date"
          color="primary"
          full-width
          header-color="#0085d0"
          no-title
          scrollable
        />
      </v-menu>
    </v-col>
    <v-col cols="6">
      <v-menu
        v-model="menu2"
        activator="parent"
        :close-on-content-click="false"
        min-width="auto"
        offset-y
        transition="scale-transition"
      >
        <template #activator="{ props }">
          <v-text-field
            v-model="time"
            :active="menu2"
            :focus="menu2"
            label="Horario"
            prepend-icon="mdi-clock"
            readonly
            v-bind="props"
            style="width: 100%;"
          />
        </template>
        <v-time-picker
          v-if="menu2"
          v-model="time"
          color="primary"
          format="24hr"
          full-width
          header-color="primary"
          use-seconds
        />
      </v-menu>
    </v-col>
  </v-row>
</template>

<script setup>
  // Variables reactivas para la fecha, los menús de selección y la hora
  const date = ref(null) // Almacena la fecha seleccionada
  const menu = ref(false) // Controla la visibilidad del menú del selector de fecha
  const menu2 = ref(false) // Controla la visibilidad del menú del selector de hora
  const time = ref(null) // Almacena la hora seleccionada

  // Propiedad computada para formatear la fecha a 'dd/mm/yyyy'
  const formattedDate = computed(() => {
    if (!date.value) return null // Si no hay fecha, retorna nulo
    const d = new Date(date.value)
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0') // Añade cero inicial si es necesario
    const day = String(d.getDate()).padStart(2, '0') // Añade cero inicial si es necesario
    return `${day}/${month}/${year}` // Formato de fecha
  })

  // Observadores para cerrar los menús cuando se selecciona una fecha u hora
  watch(date, () => {
    menu.value = false // Cierra el menú de fecha al seleccionar
  })
  watch(time, () => {
    menu2.value = false // Cierra el menú de hora al seleccionar
  })

  // Define los eventos que este componente puede emitir
  const emit = defineEmits(['update:modelValue'])

  // Observa cambios en la fecha y la hora para emitir el valor combinado
  watch([date, time], ([newDate, newTime]) => {
    // Si hay fecha y hora válidas, combina y emite el valor
    if (newDate && newTime && /^\d{2}:\d{2}:\d{2}$/.test(newTime)) {
      const d = new Date(newDate)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      const combinedDateTime = `${year}-${month}-${day}T${newTime}` // Formato ISO 8601
      emit('update:modelValue', combinedDateTime) // Emite la fecha y hora combinadas
    } else {
      emit('update:modelValue', null) // Si no es válido, emite nulo
    }
  }, { immediate: true }) // Ejecuta el observador inmediatamente al inicio
</script>

<style scoped>
/* Estilos para los selectores de fecha y hora */
.v-date-picker,
.v-time-picker,
.v-date-picker-table {
  text-align: center !important; /* Fuerza la alineación central del texto en los selectores */
}
</style>
