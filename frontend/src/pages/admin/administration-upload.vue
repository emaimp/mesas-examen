<template>
  <v-container>
    <v-card-text>
      <AdminFileUpload />
    </v-card-text>
  </v-container>
</template>

<script setup>
  import AdminFileUpload from '@/components/admin/AdminFileUpload.vue'
</script>

<route lang="yaml">
  meta:
    layout: admin
</route>
