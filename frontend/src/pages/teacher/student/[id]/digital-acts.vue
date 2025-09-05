<template>
  <v-container>
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="text-h5 text-center">Acta Digital</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="6">
            <v-text-field label="Fecha" readonly variant="outlined" />
            <v-text-field label="Carrera" readonly variant="outlined" />
            <v-text-field label="Materia" readonly variant="outlined" />
            <v-text-field label="Llamado" readonly variant="outlined" />
          </v-col>
          <v-col cols="6">
            <v-text-field label="Nota" readonly variant="outlined" />
            <v-text-field label="N° de acta" readonly variant="outlined" />
            <v-text-field label="Observación" readonly variant="outlined" />
            <v-text-field label="Asistencia" readonly variant="outlined" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn
          class="action-button"
        >
          Guardar
        </v-btn>
        <v-btn
          class="cancel-button"
          @click="goBack"
        >
          Volver
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
  import { useRouter } from 'vue-router'

  const router = useRouter()

  const goBack = () => {
    router.back()
  }
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: teacher
</route>
