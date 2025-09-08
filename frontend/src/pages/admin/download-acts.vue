<template>
  <v-container>
    <h1 class="mb-4">Mis Actas Digitales</h1>

    <v-card class="mt-4">
      <v-card-title>Actas Disponibles</v-card-title>
      <v-card-text>
        <v-data-table
          class="elevation-1"
          :headers="headers"
          item-value="id"
          :items="actas"
        >
          <template #item.action="{ item }">
            <v-btn
              color="primary"
              size="small"
              variant="outlined"
              @click="descargarActa(item)"
            >
              <v-icon left>mdi-download</v-icon>
              Descargar
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
  const actas = ref([
    {
      id: 1,
      materia: 'Matemáticas I',
      fecha: '2023-12-15',
      calificacion: 8,
    },
    {
      id: 2,
      materia: 'Física II',
      fecha: '2023-12-20',
      calificacion: 7,
    },
  ])

  const headers = [
    { title: 'Materia', key: 'materia' },
    { title: 'Fecha de Examen', key: 'fecha' },
    { title: 'Calificación', key: 'calificacion' },
    { title: 'Acción', key: 'action', sortable: false },
  ]

  const descargarActa = item => {
    console.log('Descargando acta:', item.materia)
  }
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
