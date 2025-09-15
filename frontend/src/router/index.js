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

// Preloading inteligente basado en navegación del usuario
router.beforeEach(to => {
  // Precargar rutas relacionadas basadas en el rol del usuario
  const userRole = localStorage.getItem('userRole')

  if (userRole === 'admin' && to.path.startsWith('/admin')) {
    // Precargar todas las páginas de admin para navegación casi inmediata
    setTimeout(() => {
      import('@/pages/admin/index.vue')
      import('@/pages/admin/administration-chatbot.vue')
      import('@/pages/admin/management-tables.vue')
      import('@/pages/admin/administration-tables.vue')
      import('@/pages/admin/download-acts.vue')
      import('@/pages/admin/administration-dashboard.vue')
      import('@/pages/admin/change-password.vue')
      import('@/pages/admin/administration-upload.vue')
    }, 100)
  } else if (userRole === 'student' && to.path.startsWith('/student')) {
    // Precargar páginas comunes de estudiante
    setTimeout(() => {
      import('@/pages/student/[name]/profile.vue')
      import('@/pages/student/[name]/ratings.vue')
      import('@/pages/student/[name]/tables-exam.vue')
      import('@/pages/student/[name]/tables-registered.vue')
      import('@/pages/student/[name]/change-password.vue')
    }, 100)
  } else if (userRole === 'teacher' && to.path.startsWith('/teacher')) {
    // Precargar páginas comunes de profesor
    setTimeout(() => {
      import('@/pages/teacher/[name]/profile.vue')
      import('@/pages/teacher/[name]/tables-assigned.vue')
      import('@/pages/teacher/[name]/digital-acts.vue')
      import('@/pages/teacher/[name]/change-password.vue')
    }, 100)
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
