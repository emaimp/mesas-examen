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
    // Datos: Rendimiento promedio
    careerPerformanceAverage: null,
    // Datos: Predicción de rendimiento
    careerPerformancePrediction: null,
    // Datos: Registros en mesas de examen
    careerPercentageRegistration: null,
    // Datos: Rendimiento en mesas de examen
    careerPerformanceTableExam: null,
    // Datos: Promedio de notas por materia
    careerPerformanceSubjects: null,
    // Loading states
    isLoadingPerformanceAverage: false,
    isLoadingPerformancePrediction: false,
    isLoadingPercentageRegistration: false,
    isLoadingPerformanceTableExam: false,
    isLoadingPerformanceSubjects: false,
    // Error states
    performanceAverageError: null,
    performancePredictionError: null,
    percentageRegistrationError: null,
    performanceTableExamError: null,
    performanceSubjectsError: null,
    // Timestamp de última carga
    lastLoadedPerformanceAverage: null,
    lastLoadedPerformancePrediction: null,
    lastLoadedPercentageRegistration: null,
    lastLoadedPerformanceTableExam: null,
    lastLoadedPerformanceSubjects: null,
  }),

  actions: {
    // Obtener rendimiento promedio con cache
    async fetchPerformanceAverage (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPerformanceAverage = true
      this.performanceAverageError = null

      // Revisar cache si no forceRefresh
      if (!forceRefresh) {
        const cached = getCachedData(`performanceAverage_${careerId}`)
        if (cached) {
          this.careerPerformanceAverage = cached
          this.isLoadingPerformanceAverage = false
          return cached
        }
      }

      try {
        // Import dinámico para evitar bundles grandes
        const { useRendimientoPromedioCarrera } = await import('@/services/admin/usePerformanceAverage')
        const { fetchPerformanceAverage } = useRendimientoPromedioCarrera()
        const data = await fetchPerformanceAverage(careerId)

        if (data) {
          this.careerPerformanceAverage = data
          setCachedData(`performanceAverage_${careerId}`, data)
          this.lastLoadedPerformanceAverage = Date.now()
        }
        return data
      } catch (error) {
        this.performanceAverageError = error.message || 'Error al cargar rendimiento promedio'
        console.error('Error fetching performance average:', error)
        return null
      } finally {
        this.isLoadingPerformanceAverage = false
      }
    },

    // Obtener predicción de rendimiento con cache
    async fetchPerformancePrediction (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPerformancePrediction = true
      this.performancePredictionError = null

      if (!forceRefresh) {
        const cached = getCachedData(`performancePrediction_${careerId}`)
        if (cached) {
          this.careerPerformancePrediction = cached
          this.isLoadingPerformancePrediction = false
          return cached
        }
      }

      try {
        const { usePrediccionRendimientoCarrera } = await import('@/services/admin/usePerformancePrediction')
        const { fetchPerformancePrediction } = usePrediccionRendimientoCarrera()
        const data = await fetchPerformancePrediction(careerId)

        if (data) {
          this.careerPerformancePrediction = data
          setCachedData(`performancePrediction_${careerId}`, data)
          this.lastLoadedPerformancePrediction = Date.now()
        }
        return data
      } catch (error) {
        this.performancePredictionError = error.message || 'Error al cargar predicción de rendimiento'
        console.error('Error fetching performance prediction:', error)
        return null
      } finally {
        this.isLoadingPerformancePrediction = false
      }
    },

    // Obtener registros de exámenes con cache
    async fetchPercentageRegistration (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPercentageRegistration = true
      this.percentageRegistrationError = null

      if (!forceRefresh) {
        const cached = getCachedData(`percentageRegistrations_${careerId}`)
        if (cached) {
          this.careerPercentageRegistration = cached
          this.isLoadingPercentageRegistration = false
          return cached
        }
      }

      try {
        const { usePorcentajeRegistrosCarrera } = await import('@/services/admin/usePercentageRegistration')
        const { fetchPercentageRegistration } = usePorcentajeRegistrosCarrera()
        const data = await fetchPercentageRegistration(careerId)

        if (data) {
          this.careerPercentageRegistration = data
          setCachedData(`percentageRegistrations_${careerId}`, data)
          this.lastLoadedPercentageRegistration = Date.now()
        }
        return data
      } catch (error) {
        this.percentageRegistrationError = error.message || 'Error al cargar el porcentaje de registros en mesas de examen'
        console.error('Error fetching percentage registrations:', error)
        return null
      } finally {
        this.isLoadingPercentageRegistration = false
      }
    },

    // Obtener el rendimiento en mesas de examen con cache
    async fetchPerformanceTableExam (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPerformanceTableExam = true
      this.performanceTableExamError = null

      if (!forceRefresh) {
        const cached = getCachedData(`performanceTableExam_${careerId}`)
        if (cached) {
          this.careerPerformanceTableExam = cached
          this.isLoadingPerformanceTableExam = false
          return cached
        }
      }

      try {
        const { useRendimientoMesasExamenCarrera } = await import('@/services/admin/usePerformanceTableExam')
        const { fetchPerformanceTableExam } = useRendimientoMesasExamenCarrera()
        const data = await fetchPerformanceTableExam(careerId)

        if (data) {
          this.careerPerformanceTableExam = data
          setCachedData(`performanceTableExam_${careerId}`, data)
          this.lastLoadedPerformanceTableExam = Date.now()
        }
        return data
      } catch (error) {
        this.performanceTableExamError = error.message || 'Error al cargar el rendimiento en mesas de examen'
        console.error('Error fetching performance table exam:', error)
        return null
      } finally {
        this.isLoadingPerformanceTableExam = false
      }
    },

    // Obtener el promedio de notas por materia con cache
    async fetchPerformanceSubjects (careerId, forceRefresh = false) {
      if (!careerId) {
        return null
      }

      this.isLoadingPerformanceSubjects = true
      this.performanceSubjectsError = null

      if (!forceRefresh) {
        const cached = getCachedData(`performanceSubjects_${careerId}`)
        if (cached) {
          this.careerPerformanceSubjects = cached
          this.isLoadingPerformanceSubjects = false
          return cached
        }
      }

      try {
        const { usePromedioNotasMaterias } = await import('@/services/admin/usePerformanceSubjects')
        const { fetchPerformanceSubjects } = usePromedioNotasMaterias()
        const data = await fetchPerformanceSubjects(careerId)

        if (data) {
          this.careerPerformanceSubjects = data
          setCachedData(`performanceSubjects_${careerId}`, data)
          this.lastLoadedPerformanceSubjects = Date.now()
        }
        return data
      } catch (error) {
        this.performanceSubjectsError = error.message || 'Error al cargar el promedio de notas por materia'
        console.error('Error fetching performance subjects:', error)
        return null
      } finally {
        this.isLoadingPerformanceSubjects = false
      }
    },

    // Limpiar cache específica o completa
    clearCache (type = null, careerId = null) {
      if (type === 'rendimientoPromedio' && careerId) {
        localStorage.removeItem(`adminDashboard_performanceAverage_${careerId}`)
        this.careerPerformanceAverage = null
        this.lastLoadedPerformanceAverage = null
      } else if (type === 'prediccionRendimiento' && careerId) {
        localStorage.removeItem(`adminDashboard_performancePrediction_${careerId}`)
        this.careerPerformancePrediction = null
        this.lastLoadedPerformancePrediction = null
      } else if (type === 'porcentajeInscripciones' && careerId) {
        localStorage.removeItem(`adminDashboard_percentageRegistrations_${careerId}`)
        this.careerPercentageRegistration = null
        this.lastLoadedPercentageRegistration = null
      } else if (type === 'rendimientoMesasExamen' && careerId) {
        localStorage.removeItem(`adminDashboard_performanceTableExam_${careerId}`)
        this.careerPerformanceTableExam = null
        this.lastLoadedPerformanceTableExam = null
      } else if (type === 'promedioNotasMaterias' && careerId) {
        localStorage.removeItem(`adminDashboard_performanceSubjects_${careerId}`)
        this.careerPerformanceSubjects = null
        this.lastLoadedPerformanceSubjects = null
      } else {
        // Limpiar todo el cache del store
        for (const key of Object.keys(localStorage)) {
          if (key.startsWith('adminDashboard_')) {
            localStorage.removeItem(key)
          }
        }
        this.careerPerformanceAverage = null
        this.careerPerformancePrediction = null
        this.careerPercentageRegistration = null
        this.careerPerformanceTableExam = null
        this.careerPerformanceSubjects = null
        this.lastLoadedPerformanceAverage = null
        this.lastLoadedPerformancePrediction = null
        this.lastLoadedPercentageRegistration = null
        this.lastLoadedPerformanceTableExam = null
        this.lastLoadedPerformanceSubjects = null
      }
    },

    // Verificar si data está actualizada
    isDataFresh (type) {
      const typeMap = {
        rendimientoPromedio: 'PerformanceAverage',
        prediccionRendimiento: 'PerformancePrediction',
        porcentajeInscripciones: 'PercentageRegistration',
        rendimientoMesasExamen: 'PerformanceTableExam',
        promedioNotasMaterias: 'PerformanceSubjects',
      }
      const suffix = typeMap[type] || type.charAt(0).toUpperCase() + type.slice(1)
      const lastLoaded = this[`lastLoaded${suffix}`]
      return lastLoaded && (Date.now() - lastLoaded < CACHE_TTL)
    },

    // Resetear todo el estado del store
    resetAll () {
      this.careerPerformanceAverage = null
      this.careerPerformancePrediction = null
      this.careerPercentageRegistration = null
      this.careerPerformanceTableExam = null
      this.careerPerformanceSubjects = null
      this.isLoadingPerformanceAverage = false
      this.isLoadingPerformancePrediction = false
      this.isLoadingPercentageRegistration = false
      this.isLoadingPerformanceTableExam = false
      this.isLoadingPerformanceSubjects = false
      this.performanceAverageError = null
      this.performancePredictionError = null
      this.percentageRegistrationError = null
      this.performanceTableExamError = null
      this.performanceSubjectsError = null
      this.lastLoadedPerformanceAverage = null
      this.lastLoadedPerformancePrediction = null
      this.lastLoadedPercentageRegistration = null
      this.lastLoadedPerformanceTableExam = null
      this.lastLoadedPerformanceSubjects = null
      // Opcional: limpiar cache completo del store
      this.clearCache()
    },
  },

  // Persistencia básica del estado (no cache, solo estado UI)
  persist: {
    paths: ['lastLoadedPerformanceAverage', 'lastLoadedPerformancePrediction', 'lastLoadedPercentageRegistration', 'lastLoadedPerformanceTableExam'],
  },
})
