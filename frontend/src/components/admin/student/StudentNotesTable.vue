<template>
  <v-expansion-panel>
    <v-expansion-panel-title class="text-h6">
      Notas del Estudiante
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <div>
        <v-table density="compact">
          <thead>
            <tr>
              <th class="text-left small-text">Materia</th>
              <th class="text-left small-text">1° Evaluación</th>
              <th class="text-left small-text">Recuperatorio</th>
              <th class="text-left small-text">2° Evaluación</th>
              <th class="text-left small-text">Recuperatorio</th>
              <th class="text-left small-text">3° Evaluación</th>
              <th class="text-left small-text">Recuperatorio</th>
              <th class="text-left small-text">Promedio</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="nota in notasData" :key="nota.id">
              <td class="text-left">{{ nota.materia }}</td>
              <td :class="['text-center', formatNota(nota.eval_1).class]">
                {{ formatNota(nota.eval_1).value }}
              </td>
              <td :class="['text-center', formatNota(nota.rec_1).class]">
                {{ formatNota(nota.rec_1).value }}
              </td>
              <td :class="['text-center', formatNota(nota.eval_2).class]">
                {{ formatNota(nota.eval_2).value }}
              </td>
              <td :class="['text-center', formatNota(nota.rec_2).class]">
                {{ formatNota(nota.rec_2).value }}
              </td>
              <td :class="['text-center', formatNota(nota.eval_3).class]">
                {{ formatNota(nota.eval_3).value }}
              </td>
              <td :class="['text-center', formatNota(nota.rec_3).class]">
                {{ formatNota(nota.rec_3).value }}
              </td>
              <td :class="['text-center', formatNota(nota.nota_prom).class]">
                {{ formatNota(nota.nota_prom).value }}
              </td>
            </tr>
          </tbody>
        </v-table>
        <v-divider class="my-4" />
      </div>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<script setup>
  // Define las propiedades que este componente puede recibir
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const props = defineProps({
    notasData: {
      type: Array,
      required: true, // notasData es una propiedad requerida
      // Validador para asegurar que cada elemento en notasData tenga la estructura esperada
      validator: value => {
        return Array.isArray(value) && value.every(nota =>
          (typeof nota.id === 'number' || nota.id === null || typeof nota.id === 'string' || nota.id === undefined)
          && (typeof nota.estudiante_id === 'number' || nota.estudiante_id === null || typeof nota.estudiante_id === 'string' || nota.estudiante_id === undefined)
          && (typeof nota.materia_carrera_id === 'number' || nota.materia_carrera_id === null || typeof nota.materia_carrera_id === 'string' || nota.materia_carrera_id === undefined)
          && (typeof nota.eval_1 === 'number' || nota.eval_1 === null || typeof nota.eval_1 === 'string' || nota.eval_1 === undefined)
          && (typeof nota.rec_1 === 'number' || nota.rec_1 === null || typeof nota.rec_1 === 'string' || nota.rec_1 === undefined)
          && (typeof nota.eval_2 === 'number' || nota.eval_2 === null || typeof nota.eval_2 === 'string' || nota.eval_2 === undefined)
          && (typeof nota.rec_2 === 'number' || nota.rec_2 === null || typeof nota.rec_2 === 'string' || nota.rec_2 === undefined)
          && (typeof nota.eval_3 === 'number' || nota.eval_3 === null || typeof nota.eval_3 === 'string' || nota.eval_3 === undefined)
          && (typeof nota.rec_3 === 'number' || nota.rec_3 === null || typeof nota.rec_3 === 'string' || nota.rec_3 === undefined)
          && (typeof nota.nota_prom === 'number' || nota.nota_prom === null || typeof nota.nota_prom === 'string' || nota.nota_prom === undefined),
        )
      },
    },
  })

  /**
   * Formatea una nota y asigna una clase CSS basada en su valor.
   * @param {number|string|null|undefined} nota - La nota a formatear.
   * @returns {{value: string, class: string}} Un objeto con la nota formateada y la clase CSS.
   */
  const formatNota = nota => {
    // Si la nota es nula, indefinida, vacía o "N/A", devuelve "N/A" con la clase 'nota-na'
    if (nota === null || nota === undefined || String(nota).trim() === '' || String(nota).toUpperCase() === 'N/A') {
      return { value: 'N/A', class: 'nota-na' }
    }

    // Convierte la nota a número
    const notaNum = Number.parseFloat(nota)
    let className = ''

    // Asigna una clase CSS según el valor numérico de la nota
    if (Number.isNaN(notaNum)) {
      // Si no es un número válido, devuelve la nota original con la clase 'nota-na'
      return { value: String(nota), class: 'nota-na' }
    } else if (notaNum >= 7) {
      // Nota aprobada (7 o más)
      className = 'nota-aprobada'
    } else if (notaNum >= 4) {
      // Nota regular (entre 4 y 6.99)
      className = 'nota-regular'
    } else {
      // Nota desaprobada (menos de 4)
      className = 'nota-desaprobada'
    }

    // Devuelve el valor de la nota y la clase asignada
    return { value: String(notaNum), class: className }
  }
</script>

<style scoped>
/* Estilos para el panel de expansión */
.v-expansion-panel {
  background-color: transparent !important; /* Hace que el panel tenga un fondo transparente */
  margin-bottom: 10px; /* Añade espacio entre paneles */
}

/* Estilos para la tabla dentro del panel */
.v-table {
  background-color: transparent !important; /* La tabla dentro del contenido también es transparente */
}

/* Clase para reducir el tamaño del texto en los encabezados de la tabla */
.small-text {
  font-size: 1rem !important; /* Ajusta el tamaño de fuente según sea necesario */
  font-weight: bold !important; /* Resalta el texto del encabezado */
}

/* Estilos para las notas */
.nota-aprobada {
  color: #4CAF50 !important; /* Verde para notas aprobadas (7 o más) */
  font-weight: bold;
}

.nota-regular {
  color: #FFC107 !important; /* Amarillo/Naranja para notas regulares (4 a 6.99) */
  font-weight: bold;
}

.nota-desaprobada {
  color: #FF2F1E !important; /* Rojo para notas desaprobadas (menos de 4) */
  font-weight: bold;
}

.nota-na {
  color: #9E9E9E !important; /* Gris para "N/A" */
}
</style>
