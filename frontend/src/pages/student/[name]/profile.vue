<template>
  <v-container>
    <LoggedInStudentCard />
  </v-container>
</template>

<script setup>
  import LoggedInStudentCard from '@/components/student/StudentCardLogin.vue'
</script>

<route lang="yaml">
  name: student
  meta:
    layout: student
</route>
