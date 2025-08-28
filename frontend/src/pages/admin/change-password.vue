<template>
  <v-container>
    <v-card-text>
      <ChangePassword />
    </v-card-text>
  </v-container>
</template>

<script setup>
  import ChangePassword from '@/components/ChangePassword.vue'
</script>

<route lang="yaml">
  meta:
    layout: admin
</route>
