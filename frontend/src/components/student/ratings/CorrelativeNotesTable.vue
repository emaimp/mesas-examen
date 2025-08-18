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
              <td class="text-center">{{ formatNota(materia.nota_prom) }}</td>
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
   * Formatea una nota para mostrar "N/A" si es nula, indefinida, vacía o "N/A"
   * @param {number|string|null|undefined} nota - La nota a formatear
   * @returns {string} La nota formateada o "N/A"
   */
  const formatNota = nota => {
    if (nota === null || nota === undefined || String(nota).trim() === '' || String(nota).toUpperCase() === 'N/A') {
      return 'N/A'
    }
    return String(nota)
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
</style>
