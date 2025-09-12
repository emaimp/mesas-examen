<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card width="900">
      <v-card-title class="text-center mb-4 mt-4">Mesas de Examen Inscriptas</v-card-title>
      <v-card-text>
        <ExamRegisteredPanel />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
  import ExamRegisteredPanel from '@/components/student/examtables/ExamRegisteredPanel.vue'
</script>

<route lang="yaml">
  meta:
    layout: student
</route>
