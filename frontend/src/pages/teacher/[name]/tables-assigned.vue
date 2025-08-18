<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card width="900">
      <v-card-title class="text-center mb-4 mt-4">Estudiantes Asignados</v-card-title>
      <v-card-text>
        <StudentRegisteredPanel />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
  import StudentRegisteredPanel from '@/components/teacher/examtables/StudentRegisteredPanel.vue'
</script>

<route lang="yaml">
  meta:
    layout: teacher
</route>
