<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card width="900">
      <v-card-title class="text-center mb-4 mt-4">Gestión de Mesas</v-card-title>
      <v-card-text>
        <div>
          <div v-if="loading" class="text-center py-5">
            <v-progress-circular color="primary" indeterminate />
            <p class="mt-2 text-white">Cargando...</p>
          </div>

          <v-alert
            v-else-if="
              !loading &&
                (!mesasAgrupadasPorCarrera || Object.keys(mesasAgrupadasPorCarrera).length === 0)
            "
            class="mb-4"
            text="No hay mesas de examen disponibles."
            type="info"
            variant="tonal"
          />

          <v-expansion-panels
            v-else
            v-model="openPanels"
            variant="accordion"
          >
            <v-expansion-panel
              v-for="carreraData in sortedMesasAgrupadasPorCarrera"
              :key="carreraData.carrera_nombre"
            >
              <v-expansion-panel-title class="text-h6">
                {{ carreraData.carrera_nombre }}
              </v-expansion-panel-title>

              <v-expansion-panel-text>
                <div class="transparent-expansion-panel-content">
                  <v-row dense>
                    <ExamTableCard
                      v-for="mesaLlamado in flatMesasPorLlamado(carreraData.mesas)"
                      :key="mesaLlamado.unique_key"
                      action-type="delete"
                      :mesa="mesaLlamado"
                      @open-delete-dialog="openDeleteDialog"
                    />
                  </v-row>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="showDeleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 text-center mt-2 mx-2">
          Confirmar Eliminación
        </v-card-title>
        <v-card-text v-if="selectedMesaToDelete">
          Deseas eliminar la siguiente mesa de examen?
          <v-list dense>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Materia:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesaToDelete.materia_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Profesor:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesaToDelete.profesor_nombre
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Llamado:</v-list-item-title>
              <v-list-item-subtitle>{{
                selectedMesaToDelete.tipo_llamado
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">Fecha y Hora:</v-list-item-title>
              <v-list-item-subtitle>{{
                formatFechaHora(selectedMesaToDelete.fecha)
              }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions class="mb-2 mx-2">
          <v-spacer />
          <v-btn
            class="action-button"
            :disabled="deleteLoading[selectedMesaToDelete?.id]"
            :loading="deleteLoading[selectedMesaToDelete?.id]"
            variant="outlined"
            @click="confirmDelete"
          >
            Eliminar
          </v-btn>
          <v-btn
            class="cancel-button"
            variant="text"
            @click="showDeleteDialog = false"
          >
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="snackbar.show"
      class="centered-snackbar"
      :color="snackbar.color"
      timeout="6000"
    >
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
  import ExamTableCard from '../../components/student/examtables/ExamTableCard.vue'
  import { useAdminTablesStore } from '../../stores/adminTables.js'

  // Inicializa el store de tablas admin
  const adminTablesStore = useAdminTablesStore()

  // Watcher para cambios en el contador de actualizaciones de mesas
  watch(() => adminTablesStore.changeCounter, (newVal, oldVal) => {
    if (newVal > oldVal && oldVal !== undefined) {
      // Fuerza recarga si el contador cambió (debido a creación o eliminación en otra vista)
      adminTablesStore.fetchExamTablesGrouped(true)
    }
  })

  // Propiedades reactivas para el estado del componente
  const openPanels = ref([]) // Controla qué paneles de expansión están abiertos
  const showDeleteDialog = ref(false) // Controla la visibilidad del diálogo de eliminación
  const selectedMesaToDelete = ref(null) // Mesa de examen seleccionada para eliminación
  const deleteLoading = ref({}) // Estado de carga para eliminaciones individuales
  const snackbar = ref({ // Controla la visibilidad y contenido de los mensajes de notificación
    show: false,
    message: '',
    color: '',
  })

  // Estados del store (reutilizados)
  const mesasAgrupadasPorCarrera = computed(() => adminTablesStore.examTablesGrouped || [])
  const loading = computed(() => adminTablesStore.isLoadingTables)

  // Propiedad computada para ordenar las mesas por carrera
  const sortedMesasAgrupadasPorCarrera = computed(() => {
    if (!Array.isArray(mesasAgrupadasPorCarrera.value)) {
      return []
    }
    // Ordena las mesas de examen por nombre de carrera de forma ascendente
    return [...mesasAgrupadasPorCarrera.value].sort(
      (a, b) => a.carrera_nombre.localeCompare(b.carrera_nombre),
    )
  })

  // Función para aplanar y separar las mesas por llamado
  const flatMesasPorLlamado = mesas => {
    const allLlamados = []
    // Verifica si mesas es un array
    if (Array.isArray(mesas)) {
      // Itera sobre cada mesa de examen
      for (const mesa of mesas) {
        // Si existe un primer llamado, lo añade a la lista
        if (mesa.primer_llamado) {
          allLlamados.push({
            ...mesa,
            fecha: mesa.primer_llamado,
            tipo_llamado: 'Primer Llamado',
            unique_key: `${mesa.id}_primer`,
          })
        }
        // Si existe un segundo llamado, lo añade a la lista
        if (mesa.segundo_llamado) {
          allLlamados.push({
            ...mesa,
            fecha: mesa.segundo_llamado,
            tipo_llamado: 'Segundo Llamado',
            unique_key: `${mesa.id}_segundo`,
          })
        }
      }
    }
    // Retorna todos los llamados aplanados
    return allLlamados
  }

  /**
   * Formatea una cadena de fecha ISO a un formato legible en español
   * @param {string} isoString - La cadena de fecha en formato ISO
   * @returns {string} La fecha y hora formateada
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
   * Abre el diálogo de eliminación y establece la mesa seleccionada
   * @param {Object} mesa - El objeto de la mesa de examen a eliminar
   */
  const openDeleteDialog = mesa => {
    selectedMesaToDelete.value = mesa
    showDeleteDialog.value = true
  }

  /**
   * Confirma la eliminación de la mesa de examen seleccionada
   */
  const confirmDelete = async () => {
    if (!selectedMesaToDelete.value) {
      snackbar.value = {
        show: true,
        message: 'Error: No hay mesa seleccionada para eliminar.',
        color: 'error',
      }
      showDeleteDialog.value = false
      return
    }

    const mesaId = selectedMesaToDelete.value.id
    deleteLoading.value = { ...deleteLoading.value, [mesaId]: true }

    try {
      await adminTablesStore.deleteExamTable(mesaId)
      snackbar.value = {
        show: true,
        message: 'Mesa de examen eliminada exitosamente.',
        color: 'success',
      }
      // El store maneja la limpieza automática del cache
    } catch (error) {
      console.error('Error al eliminar mesa de examen:', error)
      snackbar.value = {
        show: true,
        message: error.message || 'Ocurrió un error al eliminar la mesa de examen.',
        color: 'error',
      }
    } finally {
      deleteLoading.value = { ...deleteLoading.value, [mesaId]: false }
      showDeleteDialog.value = false
    }
  }

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(async () => {
    await adminTablesStore.fetchExamTablesGrouped() // Carga las mesas desde el store con cache
    // Abre el primer panel si hay mesas disponibles
    openPanels.value = sortedMesasAgrupadasPorCarrera.value.length > 0 ? [0] : []
  })
</script>

<style scoped>
/* Estilos para los paneles de expansión */
.v-expansion-panel {
  background-color: transparent !important; /* Fondo transparente */
  margin-bottom: 5px; /* Margen inferior */
}

/* Estilos para el contenido dentro de los paneles de expansión */
.transparent-expansion-panel-content {
  padding: 6px; /* Relleno interno */
}

/* Estilos para la barra de notificación (snackbar) */
.centered-snackbar {
  left: 50% !important; /* Centra horizontalmente */
  transform: translateX(-50%) !important; /* Ajuste para centrado perfecto */
  bottom: 0 !important; /* Alinea en la parte inferior */
  text-align: center; /* Centra el texto */
}

/* Estilos para sobreescribir el .v-list global */
.v-list {
  background: linear-gradient(to right bottom, #003356, #111c35) !important;
}
</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
