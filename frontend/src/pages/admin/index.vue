<template>
  <v-container max-width="1200">
    <div>
      <v-img
        class="mb-10 mx-auto"
        height="250"
        max-width="500"
        src="@/assets/iesn6_logo.png"
      />
      <v-row justify="center">
        <v-col
          v-for="link in links"
          :key="link.href"
          class="d-flex justify-center"
          cols="10"
          lg="5"
          md="5"
          sm="5"
        >
          <v-card
            append-icon="mdi-open-in-new"
            class="py-1 transparent-card-custom fixed-card-size"
            :href="link.href"
            :prepend-icon="link.icon"
            rel="noopener noreferrer"
            rounded="lg"
            :subtitle="link.subtitle"
            target="_blank"
            :title="link.title"
          />
        </v-col>
      </v-row>
    </div>
    <div class="fab-container">
      <AdminFileUpload />
    </div>
  </v-container>
</template>

<script setup>
  import AdminFileUpload from '@/components/admin/AdminFileUpload.vue'

  // Define un array de objetos para los enlaces de la página
  const links = [
    {
      href: 'https://ifdc6m-juj.infd.edu.ar/sitio/', // URL del enlace
      icon: 'mdi-school', // Icono de Material Design para el enlace
      subtitle: 'Página oficial del Instituto.', // Subtítulo descriptivo
      title: 'Instituto', // Título del enlace
    },
    {
      href: '', // URL vacía, para documentación futura
      icon: 'mdi-file-document', // Icono de Material Design para el enlace
      subtitle: 'Página de la documentación.', // Subtítulo descriptivo
      title: 'Documentación', // Título del enlace
    },
  ]
</script>

<style scoped>
/* Estilos para las tarjetas de tamaño fijo */
.fixed-card-size {
  width: 450px; /* Ancho fijo */
  height: 85px; /* Altura fija */
}

/* Estilos para el contenedor del botón de acción flotante (FAB) */
.fab-container {
  position: fixed; /* Posicionamiento fijo en la pantalla */
  bottom: 60px; /* Distancia desde la parte inferior */
  right: 870px; /* Distancia desde la parte derecha */
  z-index: 1000; /* Asegura que esté por encima de otros elementos */
}
</style>

<route lang="yaml">
  name: admin
  meta:
    layout: admin
</route>
