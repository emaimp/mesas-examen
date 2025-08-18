<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col class="text-center" cols="12">
        <img alt="Repair Icon" class="repair-icon" src="@/assets/repair.png">
        <h2 class="mt-4">Página en Construcción</h2>
        <p>Estamos trabajando para traer esta funcionalidad pronto.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>

</script>

<style scoped>
.repair-icon {
  max-width: 200px; /* Ajusta el tamaño del icono según sea necesario */
  height: auto;
  display: block;
  margin: 0 auto; /* Centra la imagen horizontalmente */
}

.text-center {
  text-align: center;
}
</style>

<route lang="yaml">
  meta:
    layout: student
</route>
