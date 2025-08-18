<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card width="900">
      <v-card-title class="text-center mb-4 mt-4">Mesas de Examen</v-card-title>
      <v-card-text>
        <ExamTablePanel />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
  import ExamTablePanel from '@/components/student/examtables/ExamTablePanel.vue'
</script>

<route lang="yaml">
  meta:
    layout: student
</route>
