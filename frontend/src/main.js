/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Composables
import { createApp } from 'vue'
// Plugins
import VueApexCharts from 'vue3-apexcharts'
import { registerPlugins } from '@/plugins'
// Components
import App from './App.vue'
// Styles
import 'unfonts.css'

const app = createApp(App)

registerPlugins(app)

// Registrar ApexCharts globalmente
app.component('apexchart', VueApexCharts)

app.mount('#app')
