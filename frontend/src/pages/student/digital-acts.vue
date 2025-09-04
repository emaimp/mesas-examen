<template>
  <v-container>
    <h1 class="mb-4">Mis Actas Digitales</h1>

    <v-card class="mt-4">
      <v-card-title>Actas Disponibles</v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="actas"
          item-value="id"
          class="elevation-1"
        >
          <template v-slot:item.action="{ item }">
            <v-btn
              color="primary"
              variant="outlined"
              size="small"
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
import { ref } from 'vue'; // ¡Esta línea es la que faltaba!

const actas = ref([
  // Datos de ejemplo. Aquí se cargarán las actas del estudiante desde el backend
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
]);

const headers = [
  { title: 'Materia', key: 'materia' },
  { title: 'Fecha de Examen', key: 'fecha' },
  { title: 'Calificación', key: 'calificacion' },
  { title: 'Acción', key: 'action', sortable: false },
];

const descargarActa = (item) => {
  console.log('Descargando acta:', item.materia);
  // Aquí irá la lógica para solicitar y descargar el PDF del acta
};
</script>

<style scoped>
/* Puedes añadir estilos específicos si es necesario */
</style>

---

##Pasos finales

1.  **Guarda** el archivo.
2.  **Reinicia el servidor de desarrollo** (`Ctrl + C` y luego `npm run dev`).

Una vez que el servidor se reinicie, los errores desaparecerán y la interfaz para estudiantes se mostrará correctamente.