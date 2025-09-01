<template>
  <v-container>
    <v-card-text>
      <ChatBotPanel />
    </v-card-text>
  </v-container>
</template>

<script setup>
  import ChatBotPanel from '@/components/chatbot/ChatBotPanel.vue'
</script>

<route lang="yaml">
  meta:
    layout: admin
</route>
