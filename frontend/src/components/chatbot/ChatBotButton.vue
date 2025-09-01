<template>
  <div class="chatbot-button-container">
    <v-btn
      class="chatbot-button"
      icon
      @click="navigateToChatbotPage"
    >
      <v-icon color="#ffffff" size="70">mdi-robot</v-icon>
    </v-btn>
  </div>
</template>

<script setup>
  import { useRouter } from 'vue-router'

  const router = useRouter()

  const navigateToChatbotPage = () => {
    router.push('/admin/administration-chatbot')
  }
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
  border: 2px solid; /* Borde blanco */
}
</style>
