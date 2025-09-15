import { defineStore } from 'pinia'

export const useTeacherDigitalActsStore = defineStore('teacherDigitalActs', {
  state: () => ({
    digitalActsUpdated: 0, // Counter to trigger reactivity
  }),

  actions: {
    /* Esto dispara la actualización en otros componentes */
    notifyGradeUpdate () {
      this.digitalActsUpdated++
    },

    /* Reset de la notificación (por si es necesario) */
    resetNotification () {
      this.digitalActsUpdated = 0
    },
  },

  getters: {
    /* Retorna true si hay cambios pendientes de actualización */
    hasPendingUpdate: state => state.digitalActsUpdated > 0,

    /* Obtiene la versión actual del estado */
    updateVersion: state => state.digitalActsUpdated,
  },
})
