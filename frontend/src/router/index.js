/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Decodifica tokens JWT (autenticación)
import { jwtDecode } from 'jwt-decode'
// Composables
import { setupLayouts } from 'virtual:generated-layouts'
import { createRouter, createWebHistory } from 'vue-router/auto'
import { routes } from 'vue-router/auto-routes'

// Usar rutas auto-generadas que ya incluyen lazy loading
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL, { base: '/' }), // Establecer explícitamente la base a '/'
  routes: [
    ...setupLayouts(routes), // Rutas auto-generadas con lazy loading automático
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

// Guard de autenticación para proteger rutas y gestionar login
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  // Si se intenta acceder a login estando autenticado se redirecciona al layout
  if (to.name === '/login/' && token) {
    try {
      const decoded = jwtDecode(token)
      const role = decoded.role

      switch (role) {
        case 'admin': {
          return next({ name: 'admin' })
        }
        case 'teacher': {
          return next({ name: 'teacher', params: { name: decoded.nombre } })
        }
        case 'student': {
          return next({ name: 'student', params: { name: decoded.nombre } })
        }
        default: {
          // Rol desconocido, limpiar token
          localStorage.removeItem('access_token')
          return next()
        }
      }
    } catch {
      // Token inválido, limpiar
      localStorage.removeItem('access_token')
      return next()
    }
  }

  // Si se intenta acceder a rutas protegidas sin token se redirecciona a login
  const publicRoutes = ['/login/', '/']
  if (!publicRoutes.includes(to.name) && !token) {
    return next({ name: '/login/' })
  }

  next()
})

// Limpia flag-errores de módulos dinámicos Vite (usado en router.onError)
router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
