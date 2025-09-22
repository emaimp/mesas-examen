/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { setupLayouts } from 'virtual:generated-layouts'
// eslint-disable-next-line import/no-duplicates
import { createRouter, createWebHistory } from 'vue-router/auto'
// eslint-disable-next-line import/no-duplicates
import { routes } from 'vue-router/auto-routes'

// Usar rutas auto-generadas que ya incluyen lazy loading
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL, { base: '/' }), // Establecer explícitamente la base a '/'
  routes: [
    ...setupLayouts(routes), // Usar rutas auto-generadas con lazy loading automático
  ],
  // Configuraciones de performance
  scrollBehavior (to, savedPosition) {
    // 1. Restaurar la posición de desplazamiento guardada
    if (savedPosition) {
      return savedPosition
    }
    // 2. Desplazarse a un ancla (hash) en la URL
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    // 3. Desplazarse al inicio de la página por defecto
    return { top: 0, behavior: 'smooth' }
  },
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError(err => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (localStorage.getItem('vuetify:dynamic-reload')) {
      console.error('Dynamic import error, reloading page did not fix it', err)
    } else {
      console.log('Reloading page to fix dynamic import error (temporarily disabled)')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      // location.assign(to.fullPath) // Deshabilitado temporalmente para depuración
    }
  } else {
    console.error(err)
  }
})

// Mapa para rastrear rutas ya precargadas (evita duplicados y sobrecarga)
const preloadedRoutes = new Set()
// Límite de precargas simultáneas para no bloquear recursos
const MAX_CONCURRENT_PRELOADS = 3
let currentPreloads = 0

// Función para precargar rutas de forma inteligente usando requestIdleCallback
const preloadRoutes = async routesToPreload => {
  // Si ya se alcanzó el límite de precargas simultáneas, esperar
  if (currentPreloads >= MAX_CONCURRENT_PRELOADS) {
    return
  }

  // Filtrar rutas no precargadas
  const routes = routesToPreload.filter(route => !preloadedRoutes.has(route))

  if (routes.length === 0) {
    return
  }

  // Usar requestIdleCallback para tiempo de inactividad del navegador
  const preloadInIdle = () => {
    if (window.requestIdleCallback) {
      window.requestIdleCallback(() => performPreloads(routes), { timeout: 2000 })
    } else {
      // Fallback a setTimeout si no está disponible (IE, viejos browsers)
      setTimeout(() => performPreloads(routes), 1000)
    }
  }

  const performPreloads = async routes => {
    for (const route of routes) {
      if (currentPreloads >= MAX_CONCURRENT_PRELOADS) {
        break
      }
      if (preloadedRoutes.has(route)) {
        continue
      }

      currentPreloads++
      try {
        await router.resolve(route) // Resuelve la ruta sin cambiarla
        preloadedRoutes.add(route)
      } catch (error) {
        console.warn(`Failed to preload route ${route}:`, error)
      } finally {
        currentPreloads--
      }
    }
  }

  preloadInIdle()
}

// Preloading inteligente basado en navegación del usuario
// Solo precarga rutas críticas de forma asíncrona, no forzadamente
router.beforeEach(to => {
  // Detectar conexión lenta para saltar precargas agresivas
  const isSlowConnection = navigator.connection
    && (navigator.connection.effectiveType === 'slow-2g'
      || navigator.connection.effectiveType === '2g'
      || navigator.connection.saveData === true)

  if (isSlowConnection) {
    return // Saltar precargas en conexiones lentas
  }

  const userRole = localStorage.getItem('userRole')

  if (userRole === 'admin' && to.path.startsWith('/admin')) {
    // Precargar solo las rutas más probables/críticas en admin (no todas)
    const criticalRoutes = [
      '/admin/administration-tables', // Gestión común
      '/admin/management-tables', // Creación frecuente
      '/admin/administration-dashboard', // Dashboard para insights
    ]
    preloadRoutes(criticalRoutes)
  } else if (userRole === 'student' && to.path.startsWith('/student')) {
    // Precargar rutas comunes de estudiante, priorizando perfil y notas
    const criticalRoutes = [
      '/student/[name]/profile', // Perfil personal
      '/student/[name]/ratings', // Notas importantes
    ]
    preloadRoutes(criticalRoutes)
  } else if (userRole === 'teacher' && to.path.startsWith('/teacher')) {
    // Precargar rutas críticas de profesor
    const criticalRoutes = [
      '/teacher/[name]/profile', // Perfil personal
      '/teacher/[name]/tables-assigned', // Mesas asignadas
    ]
    preloadRoutes(criticalRoutes)
  }
})

// Preloading en hover para enlaces críticos
if (typeof window !== 'undefined') {
  // Precargar al hacer hover sobre enlaces de navegación
  document.addEventListener('mouseenter', e => {
    // Asegurarse de que e.target es un Element antes de usar closest
    if (e.target && typeof e.target.closest === 'function') {
      const target = e.target.closest('a[href]')
      if (target && target.hostname === window.location.hostname) {
        const href = target.getAttribute('href')

        // Solo precargar rutas internas importantes
        if (href && (href.includes('admin') || href.includes('student') || href.includes('teacher'))
          // Usar requestIdleCallback para no bloquear UI
          && window.requestIdleCallback) {
          window.requestIdleCallback(() => {
            router.resolve(href)
          })
        }
      }
    }
  }, true)
}

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
