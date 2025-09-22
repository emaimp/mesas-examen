import { defineStore } from 'pinia'

// Función helper para cache con TTL en localStorage
const CACHE_TTL = 5 * 60 * 1000 // 5 minutos en ms

// Obtener data del cache con TTL check
function getCachedData (key) {
  const cached = localStorage.getItem(`adminDashboard_${key}`)
  if (!cached) {
    return null
  }

  const { data, timestamp } = JSON.parse(cached)
  if (Date.now() - timestamp > CACHE_TTL) {
    localStorage.removeItem(`adminDashboard_${key}`)
    return null
  }
  return data
}

// Guardar data con timestamp
function setCachedData (key, data) {
  localStorage.setItem(`adminDashboard_${key}`, JSON.stringify({
    data,
    timestamp: Date.now(),
  }))
}

// Definición del store 'adminDashboard' usando Pinia
export const useAdminDashboardStore = defineStore('adminDashboard', {
  state: () => ({
    // Datos de rendimiento gloñal de carrera
    globalPerformance: null,
    // Datos de predicción de rendimiento
    performancePrediction: null,
    // Datos de registros en exámenes
    examRegistrations: null,
    // Loading states
    isLoadingGlobalPerformance: false,
    isLoadingPrediction: false,
    isLoadingRegistrations: false,
    // Error states
    globalPerformanceError: null,
    predictionError: null,
    registrationsError: null,
    // Timestamp de última carga
    lastLoadedGlobal: null,
    lastLoadedPrediction: null,
    lastLoadedRegistrations: null,
  }),

  actions: {
    // Obtener rendimiento global con cache
    async fetchGlobalPerformance (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingGlobalPerformance = true
      this.globalPerformanceError = null

      // Revisar cache si no forceRefresh
      if (!forceRefresh) {
        const cached = getCachedData(`globalPerformance_${careerId}`)
        if (cached) {
          this.globalPerformance = cached
          this.isLoadingGlobalPerformance = false
          return cached
        }
      }

      try {
        // Import dinámico para evitar bundles grandes
        const { useRendimientoGlobalCarrera } = await import('@/services/admin/useGlobalPerformance')
        const { fetchGlobalPerformance } = useRendimientoGlobalCarrera()
        const data = await fetchGlobalPerformance(careerId)

        if (data) {
          this.globalPerformance = data
          setCachedData(`globalPerformance_${careerId}`, data)
          this.lastLoadedGlobal = Date.now()
        }
        return data
      } catch (error) {
        this.globalPerformanceError = error.message || 'Error al cargar rendimiento global'
        console.error('Error fetching global performance:', error)
        return null
      } finally {
        this.isLoadingGlobalPerformance = false
      }
    },

    // Obtener predicción de rendimiento con cache
    async fetchPerformancePrediction (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPrediction = true
      this.predictionError = null

      if (!forceRefresh) {
        const cached = getCachedData(`prediction_${careerId}`)
        if (cached) {
          this.performancePrediction = cached
          this.isLoadingPrediction = false
          return cached
        }
      }

      try {
        const { usePredictionPerformance } = await import('@/services/admin/usePredictionPerformance')
        const { fetchPredictedPerformance } = usePredictionPerformance()
        const data = await fetchPredictedPerformance(careerId)

        if (data) {
          this.performancePrediction = data
          setCachedData(`prediction_${careerId}`, data)
          this.lastLoadedPrediction = Date.now()
        }
        return data
      } catch (error) {
        this.predictionError = error.message || 'Error al cargar predicción de rendimiento'
        console.error('Error fetching performance prediction:', error)
        return null
      } finally {
        this.isLoadingPrediction = false
      }
    },

    // Obtener registros de exámenes con cache
    async fetchExamRegistrations (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingRegistrations = true
      this.registrationsError = null

      if (!forceRefresh) {
        const cached = getCachedData(`registrations_${careerId}`)
        if (cached) {
          this.examRegistrations = cached
          this.isLoadingRegistrations = false
          return cached
        }
      }

      try {
        const { useGlobalRegistrations } = await import('@/services/admin/useGlobalRegistrations')
        const { fetchRegistrationsByCareer } = useGlobalRegistrations()
        const data = await fetchRegistrationsByCareer(careerId)

        if (data) {
          this.examRegistrations = data
          setCachedData(`registrations_${careerId}`, data)
          this.lastLoadedRegistrations = Date.now()
        }
        return data
      } catch (error) {
        this.registrationsError = error.message || 'Error al cargar registros de exámenes'
        console.error('Error fetching exam registrations:', error)
        return null
      } finally {
        this.isLoadingRegistrations = false
      }
    },

    // Limpiar cache específica o completa
    clearCache (type = null, careerId = null) {
      if (type === 'global' && careerId) {
        localStorage.removeItem(`adminDashboard_globalPerformance_${careerId}`)
        this.globalPerformance = null
        this.lastLoadedGlobal = null
      } else if (type === 'prediction' && careerId) {
        localStorage.removeItem(`adminDashboard_prediction_${careerId}`)
        this.performancePrediction = null
        this.lastLoadedPrediction = null
      } else if (type === 'registrations' && careerId) {
        localStorage.removeItem(`adminDashboard_registrations_${careerId}`)
        this.examRegistrations = null
        this.lastLoadedRegistrations = null
      } else {
        // Limpiar todo el cache del store
        for (const key of Object.keys(localStorage)) {
          if (key.startsWith('adminDashboard_')) {
            localStorage.removeItem(key)
          }
        }
        this.globalPerformance = null
        this.performancePrediction = null
        this.examRegistrations = null
        this.lastLoadedGlobal = null
        this.lastLoadedPrediction = null
        this.lastLoadedRegistrations = null
      }
    },

    // Verificar si data está actualizada
    isDataFresh (type) {
      const lastLoaded = this[`lastLoaded${type.charAt(0).toUpperCase() + type.slice(1)}`]
      return lastLoaded && (Date.now() - lastLoaded < CACHE_TTL)
    },
  },

  // Persistencia básica del estado (no cache, solo estado UI)
  persist: {
    paths: ['lastLoadedGlobal', 'lastLoadedPrediction', 'lastLoadedRegistrations'],
  },
})
