<template>
  <v-expansion-panel>
    <v-expansion-panel-title class="text-h6">
      {{ getAnioText(anioData.anio) }}
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <div>
        <v-table density="compact">
          <thead>
            <tr>
              <th class="text-center small-text">Código</th>
              <th class="text-left small-text">Materia</th>
              <th class="text-center small-text">Promedio</th>
              <th class="text-center small-text">Correlativas</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="materia in anioData.materias" :key="materia.codigo">
              <td class="text-center">{{ materia.codigo }}</td>
              <td class="text-left">{{ materia.materia }}</td>
              <td :class="['text-center', formatNota(materia.nota_prom).class]">
                {{ formatNota(materia.nota_prom).value }}
              </td>
              <td class="text-center">{{ formatCorrelativas(materia.correlativas) }}</td>
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
    anioData: { // Objeto que contiene los datos de las materias para un año específico
      type: Object,
      required: true,
      // Validador para asegurar que anioData tiene la estructura esperada
      validator: value => {
        return value && typeof value.anio === 'number' && Array.isArray(value.materias)
      },
    },
  })

  /**
   * Convierte un número de año a un texto descriptivo (ej. "1° Año")
   * @param {number} anio - El número del año
   * @returns {string} El texto del año
   */
  const getAnioText = anio => {
    if (typeof anio !== 'number' || anio <= 0 || Number.isNaN(anio)) {
      return 'Año Desconocido'
    }
    return `${anio}° Año`
  }

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

  /**
   * Formatea un array de correlativas en una cadena separada por guiones
   * @param {Array<string>} correlativas - Array de nombres de materias correlativas
   * @returns {string} La cadena formateada de correlativas o "N/A"
   */
  const formatCorrelativas = correlativas => {
    if (!correlativas || correlativas.length === 0) {
      return 'N/A'
    }
    return correlativas.join(' - ')
  }
</script>

<style scoped>
/* Estilos para el panel de expansión */
.v-expansion-panel {
  background-color: transparent !important; /* Fondo transparente */
  margin-bottom: 5px; /* Margen inferior */
}

/* Estilos para la tabla */
.v-table {
  background-color: transparent !important; /* Fondo transparente */
}

/* Estilos para texto pequeño */
.small-text {
  font-size: 0.9rem !important; /* Tamaño de fuente reducido */
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
