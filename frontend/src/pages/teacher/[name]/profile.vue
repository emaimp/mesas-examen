<template>
  <v-container d-flex fill-height>
    <LoggedInTeacherCard />
  </v-container>
</template>

<script setup>
  import LoggedInTeacherCard from '@/components/teacher/TeacherCardLogin.vue'
</script>

<route lang="yaml">
  name: teacher
  meta:
    layout: teacher
</route>
