import { defineStore } from 'pinia'

export const useStudentTableStore = defineStore('studentTable', {
  state: () => ({
    registrationUpdated: 0, // Counter to trigger reactivity
  }),

  actions: {
    /* Esto dispara la actualización en otros componentes */
    notifyRegistrationChange () {
      this.registrationUpdated++
    },

    /* Reset de la notificación (por si es necesario) */
    resetNotification () {
      this.registrationUpdated = 0
    },
  },

  getters: {
    /* Retorna true si hay cambios pendientes de actualización */
    hasPendingUpdate: state => state.registrationUpdated > 0,

    /* Obtiene la versión actual del estado */
    updateVersion: state => state.registrationUpdated,
  },
})
