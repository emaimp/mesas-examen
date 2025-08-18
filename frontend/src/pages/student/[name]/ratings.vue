<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card width="900">
      <v-card-title class="text-center mb-4 mt-4">Promedios y Correlativas</v-card-title>
      <v-card-text>
        <CorrelativeNotesPanel class="mb-4" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
  import CorrelativeNotesPanel from '@/components/student/ratings/CorrelativeNotesPanel.vue'
</script>

<route lang="yaml">
  meta:
    layout: student
</route>
