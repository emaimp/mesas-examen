/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides

import { createVuetify } from 'vuetify'
import { VFileUpload } from 'vuetify/labs/VFileUpload'
import { VTimePicker } from 'vuetify/labs/VTimePicker'
// Composables
import colors from 'vuetify/lib/util/colors'
import { es } from 'vuetify/locale'
// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

export default createVuetify({
  theme: {
    // defaultTheme: 'dark',
    themes: {
      light: {
        dark: true,
        colors: {
          primary: colors.blue.lighten4,
          secondary: colors.blue.lighten4,
          surface: '#000000',
          green_color: '#2ed22e',
          yellow_color: '#ff7900',
          red_color: '#f3180b',
          border: '#FFFFFF',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: colors.blue.darken4,
          secondary: colors.blue.darken4,
          surface: '#000000',
          green_color: '#2ed22e',
          yellow_color: '#ff7900',
          red_color: '#f3180b',
          border: '#FFFFFF',
        },
      },
    },
  },
  locale: {
    locale: 'es', // Set default locale to Spanish
    messages: { es }, // Provide Spanish messages
  },
  components: {
    VTimePicker,
    VFileUpload,
  },
})
