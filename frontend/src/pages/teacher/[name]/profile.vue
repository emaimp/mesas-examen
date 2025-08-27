<template>
  <v-container>
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
