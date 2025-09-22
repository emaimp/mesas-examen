import { defineStore } from 'pinia'

// Función helper para cache con TTL en localStorage
const CACHE_TTL = 10 * 60 * 1000 // 10 minutos en ms (más tiempo ya que son tablas grandes)

// Obtener data del cache con TTL check
function getCachedData (key) {
  const cached = localStorage.getItem(`adminTables_${key}`)
  if (!cached) {
    return null
  }

  const { data, timestamp } = JSON.parse(cached)
  if (Date.now() - timestamp > CACHE_TTL) {
    localStorage.removeItem(`adminTables_${key}`)
    return null
  }
  return data
}

// Guardar data con timestamp
function setCachedData (key, data) {
  localStorage.setItem(`adminTables_${key}`, JSON.stringify({
    data,
    timestamp: Date.now(),
  }))
}

// Definición del store 'adminTables' usando Pinia
export const useAdminTablesStore = defineStore('adminTables', {
  state: () => ({
    // Datos de mesas examinadas agrupadas por carrera
    examTablesGrouped: [],
    // Loading state
    isLoadingTables: false,
    // Error state
    tablesError: null,
    // Timestamp de última carga
    lastLoadedTables: null,
  }),

  actions: {
    // Obtener mesas examinadas agrupadas con cache
    async fetchExamTablesGrouped (forceRefresh = false) {
      this.isLoadingTables = true
      this.tablesError = null

      // Revisar cache si no forceRefresh
      if (!forceRefresh) {
        const cached = getCachedData('examTablesGrouped')
        if (cached) {
          this.examTablesGrouped = cached
          this.isLoadingTables = false
          return cached
        }
      }

      try {
        // Import dinámico para evitar bundles grandes
        const { useTablesExamAdmin } = await import('@/services/admin/useTablesExamAdmin')
        const { fetchTablesExamByCareer } = useTablesExamAdmin()
        const data = await fetchTablesExamByCareer()

        if (data) {
          this.examTablesGrouped = data
          setCachedData('examTablesGrouped', data)
          this.lastLoadedTables = Date.now()
        }
        return data
      } catch (error) {
        this.tablesError = error.message || 'Error al cargar mesas de examen'
        console.error('Error fetching exam tables grouped:', error)
        return null
      } finally {
        this.isLoadingTables = false
      }
    },

    // Eliminar mesa (llama al servicio original, luego actualiza cache)
    async deleteExamTable (tableId) {
      try {
        // Import dinámico y eliminar
        const { useTablesExamAdmin } = await import('@/services/admin/useTablesExamAdmin')
        const { deleteTableExam } = useTablesExamAdmin()
        await deleteTableExam(tableId)

        // Actualizar cache removiendo la mesa eliminada
        this.clearCache() // Forzar recarga del cache después de eliminar

        return true
      } catch (error) {
        console.error('Error deleting exam table:', error)
        throw error
      }
    },

    // Limpiar cache
    clearCache () {
      // Limpiar todo el cache del store
      for (const key of Object.keys(localStorage)) {
        if (key.startsWith('adminTables_')) {
          localStorage.removeItem(key)
        }
      }
      this.examTablesGrouped = []
      this.lastLoadedTables = null
    },

    // Verificar si data está actualizada
    isDataFresh () {
      return this.lastLoadedTables && (Date.now() - this.lastLoadedTables < CACHE_TTL)
    },
  },

  // Persistencia básica del estado
  persist: {
    paths: ['lastLoadedTables'],
  },
})
