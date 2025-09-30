<template>
  <div id="n8n-chat" />
</template>

<script lang="ts" setup>
  import { createChat } from '@n8n/chat'
  import '@n8n/chat/style.css'

  let chatApp

  onMounted(() => {
    chatApp = createChat({
      webhookUrl: 'http://localhost:5678/webhook/ae016bc3-cf50-40b8-8f4a-456ed8f58fe2/chat',
      webhookConfig: {
        method: 'POST',
        headers: {},
      },
      target: '#n8n-chat',
      mode: 'window',
      chatInputKey: 'chatInput',
      chatSessionKey: 'sessionId',
      loadPreviousSession: true,
      metadata: {},
      showWelcomeScreen: false,
      defaultLanguage: 'en',
      initialMessages: [
        'Hola!👋 Mi nombre es iesito 🤓',
      ],
      i18n: {
        en: {
          title: 'Chat Bot 🤖',
          subtitle: 'Realiza tus consultas, disponible 24/7.',
          footer: '',
          getStarted: 'Nueva conversación',
          inputPlaceholder: 'Escribe un mensaje...',
          closeButtonTooltip: '',
        },
      },
      enableStreaming: false,
    })
  })

  onUnmounted(() => {
    if (chatApp) {
      chatApp.unmount()
    }
  })
</script>

<style>
.n8n-chat {
  /* COLORES */
  --chat--color-primary: #e74266;
  --chat--color-primary-shade-50: #fb5576;
  --chat--color-secondary: #0098d5;
  --chat--color-secondary-shade-50: #34aae9;
  --chat--color-white: #ffffff;
  --chat--color-light: #f2f4f8;
  --chat--color-light-shade-50: #e6e9f1;
  --chat--color-light-shade-100: #c2c5cc;
  --chat--color-medium: #d2d4d9;
  --chat--color-dark: #000000;
  --chat--color-disabled: #777980; /* Elementos deshabilitados */
  --chat--color-typing: #404040; /* Indicador "escribiendo" */

  /* BORDER */
  --chat--border-radius: 0.25rem;

  /* HEADER */
  --chat--header--background: #131321;

  /* MENSAJES */
  --chat--message--user--color: var(--chat--color-dark);
  --chat--message--user--background: var(--chat--color-white);
  --chat--message--user--border: 1px solid var(--chat--color-primary);
  --chat--message--bot--color: var(--chat--color-dark);
  --chat--message--bot--background: var(--chat--color-white);
  --chat--message--bot--border: 1px solid var(--chat--color-secondary);

  /* DIMENSIONES */
  --chat--window--width: 500px;
  --chat--window--height: 700px;

  /* TOGGLE */
  --chat--toggle--background: #131321;
  --chat--toggle--hover--background: #131321;
  --chat--toggle--active--background: #131321;
  --chat--toggle--size: 80px;
}

/* Estilos para el input */
.n8n-chat input,
.n8n-chat textarea,
.n8n-chat input[type="text"],
.n8n-chat textarea[type="text"] {
  color: var(--chat--color-dark) !important;
  background-color: var(--chat--color-white) !important;
  border: 1px solid var(--chat--color-medium) !important;
}

/* Estilos para el placeholder */
.n8n-chat input::placeholder,
.n8n-chat textarea::placeholder {
  color: var(--chat--color-medium) !important;
}

/* Estilos para el enfoque del input */
.n8n-chat input:focus,
.n8n-chat textarea:focus {
  background-color: var(--chat--color-light) !important;
  border-color: var(--chat--color-primary) !important;
}

/* Estilos para el toggle */
.n8n-chat .chat-toggle,
.n8n-chat .chat-toggle-button,
.n8n-chat [class*="toggle"],
.n8n-chat button[class*="toggle"] {
  width: var(--chat--toggle--size) !important;
  height: var(--chat--toggle--size) !important;
}
</style>
