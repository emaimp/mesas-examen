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
    // Datos de rendimiento global de carrera
    globalPerformance: null,
    // Datos de predicción de rendimiento
    globalPrediction: null,
    // Datos de registros en exámenes
    globalRegistration: null,
    // Datos de aprobación de exámenes
    globalApproved: null,
    // Loading states
    isLoadingPerformance: false,
    isLoadingPrediction: false,
    isLoadingRegistration: false,
    isLoadingApproved: false,
    // Error states
    performanceError: null,
    predictionError: null,
    registrationError: null,
    approvedError: null,
    // Timestamp de última carga
    lastLoadedPerformance: null,
    lastLoadedPrediction: null,
    lastLoadedRegistration: null,
    lastLoadedApproved: null,
  }),

  actions: {
    // Obtener rendimiento global con cache
    async fetchGlobalPerformance (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPerformance = true
      this.performanceError = null

      // Revisar cache si no forceRefresh
      if (!forceRefresh) {
        const cached = getCachedData(`globalPerformance_${careerId}`)
        if (cached) {
          this.globalPerformance = cached
          this.isLoadingPerformance = false
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
          this.lastLoadedPerformance = Date.now()
        }
        return data
      } catch (error) {
        this.performanceError = error.message || 'Error al cargar rendimiento global'
        console.error('Error fetching global performance:', error)
        return null
      } finally {
        this.isLoadingPerformance = false
      }
    },

    // Obtener predicción de rendimiento con cache
    async fetchGlobalPrediction (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPrediction = true
      this.predictionError = null

      if (!forceRefresh) {
        const cached = getCachedData(`prediction_${careerId}`)
        if (cached) {
          this.globalPrediction = cached
          this.isLoadingPrediction = false
          return cached
        }
      }

      try {
        const { usePrediccionGlobalCarrera } = await import('@/services/admin/useGlobalPrediction')
        const { fetchGlobalPrediction } = usePrediccionGlobalCarrera()
        const data = await fetchGlobalPrediction(careerId)

        if (data) {
          this.globalPrediction = data
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
    async fetchGlobalRegistration (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingRegistration = true
      this.registrationError = null

      if (!forceRefresh) {
        const cached = getCachedData(`registrations_${careerId}`)
        if (cached) {
          this.globalRegistration = cached
          this.isLoadingRegistration = false
          return cached
        }
      }

      try {
        const { useRegistroGlobalCarrera } = await import('@/services/admin/useGlobalRegistration')
        const { fetchGlobalRegistration } = useRegistroGlobalCarrera()
        const data = await fetchGlobalRegistration(careerId)

        if (data) {
          this.globalRegistration = data
          setCachedData(`registrations_${careerId}`, data)
          this.lastLoadedRegistration = Date.now()
        }
        return data
      } catch (error) {
        this.registrationError = error.message || 'Error al cargar registros de exámenes'
        console.error('Error fetching exam registrations:', error)
        return null
      } finally {
        this.isLoadingRegistration = false
      }
    },

    // Obtener aprobación de exámenes con cache
    async fetchGlobalApproved (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingApproved = true
      this.approvedError = null

      if (!forceRefresh) {
        const cached = getCachedData(`approved_${careerId}`)
        if (cached) {
          this.globalApproved = cached
          this.isLoadingApproved = false
          return cached
        }
      }

      try {
        const { useAprobadosGlobalCarrera } = await import('@/services/admin/useGlobalApproved')
        const { fetchGlobalApproved } = useAprobadosGlobalCarrera()
        const data = await fetchGlobalApproved(careerId)

        if (data) {
          this.globalApproved = data
          setCachedData(`approved_${careerId}`, data)
          this.lastLoadedApproved = Date.now()
        }
        return data
      } catch (error) {
        this.approvedError = error.message || 'Error al cargar aprobación de exámenes'
        console.error('Error fetching exam approvals:', error)
        return null
      } finally {
        this.isLoadingApproved = false
      }
    },

    // Limpiar cache específica o completa
    clearCache (type = null, careerId = null) {
      if (type === 'global' && careerId) {
        localStorage.removeItem(`adminDashboard_globalPerformance_${careerId}`)
        this.globalPerformance = null
        this.lastLoadedPerformance = null
      } else if (type === 'prediction' && careerId) {
        localStorage.removeItem(`adminDashboard_prediction_${careerId}`)
        this.globalPrediction = null
        this.lastLoadedPrediction = null
      } else if (type === 'registrations' && careerId) {
        localStorage.removeItem(`adminDashboard_registrations_${careerId}`)
        this.globalRegistration = null
        this.lastLoadedRegistration = null
      } else if (type === 'approved' && careerId) {
        localStorage.removeItem(`adminDashboard_approved_${careerId}`)
        this.globalApproved = null
        this.lastLoadedApproved = null
      } else {
        // Limpiar todo el cache del store
        for (const key of Object.keys(localStorage)) {
          if (key.startsWith('adminDashboard_')) {
            localStorage.removeItem(key)
          }
        }
        this.globalPerformance = null
        this.globalPrediction = null
        this.globalRegistration = null
        this.globalApproved = null
        this.lastLoadedPerformance = null
        this.lastLoadedPrediction = null
        this.lastLoadedRegistration = null
        this.lastLoadedApproved = null
      }
    },

    // Verificar si data está actualizada
    isDataFresh (type) {
      const lastLoaded = this[`lastLoaded${type.charAt(0).toUpperCase() + type.slice(1)}`]
      return lastLoaded && (Date.now() - lastLoaded < CACHE_TTL)
    },

    // Resetear todo el estado del store
    resetAll () {
      this.globalPerformance = null
      this.globalPrediction = null
      this.globalRegistration = null
      this.globalApproved = null
      this.isLoadingPerformance = false
      this.isLoadingPrediction = false
      this.isLoadingRegistration = false
      this.isLoadingApproved = false
      this.performanceError = null
      this.predictionError = null
      this.registrationError = null
      this.approvedError = null
      this.lastLoadedPerformance = null
      this.lastLoadedPrediction = null
      this.lastLoadedRegistration = null
      this.lastLoadedApproved = null
      // Opcional: limpiar cache completo del store
      this.clearCache()
    },
  },

  // Persistencia básica del estado (no cache, solo estado UI)
  persist: {
    paths: ['lastLoadedPerformance', 'lastLoadedPrediction', 'lastLoadedRegistration', 'lastLoadedApproved'],
  },
})
