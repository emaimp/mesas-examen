<template>
  <v-card class="d-flex flex-column" height="100%">
    <v-card-text class="flex-grow-1 overflow-y-auto pa-0">
      <v-container class="fill-height" fluid>
        <v-row class="fill-height">
          <v-col class="fill-height" cols="12">
            <div class="message-area">
              <div v-for="(msg, index) in chatHistory" :key="index" :class="['message-bubble', msg.role]">
                <p>{{ msg.content }}</p>
              </div>
              <div v-if="isLoadingBotResponse" class="message-bubble bot loading-indicator">
                <v-progress-circular
                  color="#009090"
                  indeterminate
                  size="24"
                  width="2"
                />
                <span class="ml-2">Pensando...</span>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>

    <v-card-actions class="d-flex justify-start">
      <v-textarea
        v-model="message"
        auto-grow
        autocomplete="off"
        bg-color="#009090"
        class="mr-0 mx-6"
        density="compact"
        placeholder="Escribe un mensaje..."
        rows="2"
        variant="solo"
        @keyup.enter="sendMessage"
      />
      <v-btn
        class="mr-2 mt-n3"
        color="#ffffff"
        icon
        @click="sendMessage"
      >
        <v-icon>mdi-send</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
  import { useOllamaChat } from '@/services/admin/useOllamaChat'
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const props = defineProps({
    height: {
      type: String,
      default: '100%',
    },
  })

  // Variable para almacenar el mensaje actual del usuario
  const message = ref('')
  // Historial de mensajes del chat
  const chatHistory = ref([])
  // Indicador de carga para la respuesta del bot
  const isLoadingBotResponse = ref(false)
  // Función para enviar mensajes a Ollama
  const { sendOllamaMessage } = useOllamaChat()

  // Función para enviar un mensaje
  const sendMessage = async () => {
    // Verifica que el mensaje no esté vacío
    if (message.value.trim() !== '') {
      const userMessage = message.value.trim()
      // Agrega el mensaje del usuario al historial
      chatHistory.value.push({ role: 'user', content: userMessage })
      // Limpia el campo de entrada
      message.value = ''

      await nextTick()
      // Desplaza el área de mensajes hacia abajo
      scrollToBottom()

      // Muestra el indicador de carga
      isLoadingBotResponse.value = true

      try {
        // Envía el mensaje al bot y espera la respuesta
        const botResponse = await sendOllamaMessage(userMessage)
        // Agrega la respuesta del bot al historial
        chatHistory.value.push({ role: 'bot', content: botResponse })
      } catch (error) {
        console.error('Error sending message to Ollama:', error)
        // Muestra un mensaje de error si falla la comunicación con el bot
        chatHistory.value.push({ role: 'bot', content: 'No pude obtener una respuesta en este momento.' })
      } finally {
        // Oculta el indicador de carga
        isLoadingBotResponse.value = false
        await nextTick()
        // Desplaza el área de mensajes hacia abajo nuevamente
        scrollToBottom()
      }
    }
  }

  // Función para desplazar el área de mensajes al final
  const scrollToBottom = () => {
    const messageArea = document.querySelector('.message-area')
    if (messageArea) {
      messageArea.scrollTop = messageArea.scrollHeight
    }
  }
</script>

<style scoped>
/* Área donde se muestran los mensajes del chat */
.message-area {
  height: 101%; /* Altura del área de mensajes */
  overflow-y: auto; /* Permite el desplazamiento vertical si el contenido excede la altura */
  padding: 10px; /* Espaciado interno */
  border-radius: 4px; /* Bordes redondeados */
  display: flex; /* Usa flexbox para organizar los mensajes */
  flex-direction: column; /* Organiza los mensajes en columna */
  background-color: rgba(25, 45, 57, 0.3); /* Color de fondo */
}

/* Burbuja de mensaje individual */
.message-bubble {
  max-width: 70%; /* Ancho máximo de la burbuja */
  padding: 8px 12px; /* Espaciado interno */
  border-radius: 15px; /* Bordes redondeados para la burbuja */
  margin-bottom: 8px; /* Margen inferior entre burbujas */
  word-wrap: break-word; /* Permite que las palabras largas se rompan y pasen a la siguiente línea */
}

/* Estilos para las burbujas de mensajes del usuario */
.message-bubble.user {
  background-color: #009090; /* Color de fondo para mensajes del usuario */
  align-self: flex-end; /* Alinea la burbuja a la derecha */
  text-align: right; /* Alinea el texto a la derecha */
}

/* Estilos para las burbujas de mensajes del bot */
.message-bubble.bot {
  background-color: #ffffff; /* Color de fondo para mensajes del bot */
  align-self: flex-start; /* Alinea la burbuja a la izquierda */
  text-align: left; /* Alinea el texto a la izquierda */
}

/* Indicador de carga cuando el bot está pensando */
.loading-indicator {
  display: flex; /* Usa flexbox para alinear el icono y el texto */
  align-items: center; /* Centra verticalmente los elementos */
  font-style: italic; /* Texto en cursiva */
  color: #ffffff; /* Color del texto */
}
</style>
