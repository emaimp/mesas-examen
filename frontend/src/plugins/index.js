/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

import { createPersistedState } from 'pinia-plugin-persistedstate' // NUEVO
import router from '@/router'
import pinia from '@/stores'
// Plugins
import vuetify from './vuetify'

export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
}

pinia.use(createPersistedState()) // Registrar el plugin de persistencia
