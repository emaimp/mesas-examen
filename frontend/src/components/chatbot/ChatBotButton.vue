<template>
  <div class="chatbot-button-container">
    <v-btn
      class="chatbot-button"
      icon
      @click="dialog = true"
    >
      <v-img alt="Chatbot Icon" height="90" src="/src/assets/face_smile.png" width="90" />
    </v-btn>

    <v-dialog
      v-model="dialog"
      height="850px"
      max-width="650px"
      width="100%"
    >
      <v-card class="d-flex flex-column" height="100%">
        <v-card-title class="d-flex justify-space-between align-center py-2">
          <div class="mx-auto">CHAT BOT</div>
          <v-btn class="mr-n2" icon variant="text" @click="dialog = false">
            <v-icon color="#ffffff">mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="flex-grow-1 pa-0" style="overflow: hidden;">
          <ChatbotPanel :height="'100%'" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
  import ChatbotPanel from './ChatBotPanel.vue'

  // Define una variable reactiva para controlar la visibilidad del diálogo del chatbot
  const dialog = ref(false)
</script>

<style scoped>
/* Contenedor del botón del chatbot */
.chatbot-button-container {
  position: fixed; /* Fija el botón en la pantalla */
  bottom: 60px; /* Distancia desde la parte inferior */
  right: 70px; /* Distancia desde la parte derecha */
  z-index: 9900; /* Asegura que el botón esté por encima de otros elementos */
}

/* Estilos específicos del botón del chatbot */
.chatbot-button {
  background-color: rgba(255, 255, 255, 0.0) !important; /* Fondo transparente */
  width: 100px; /* Ancho del botón */
  height: 100px; /* Alto del botón */
}
</style>
