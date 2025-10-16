<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card width="1000">
      <v-card-title class="text-center mb-4 mt-4">Promedios - Correlativas</v-card-title>
      <v-card-text>
        <CorrelativeNotesPanel />
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
