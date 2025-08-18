<template>
  <v-container class="fill-height d-flex align-center justify-center" fluid>
    <v-card class="teacher-card" :disabled="loading" :loading="loading">
      <v-card-title class="text-h6 text-center text-wrap mt-4"> <!-- Increased mt-8 for more top spacing -->
        {{ user ? user.carrera_nombre || 'Detalles del Profesor' : 'Detalles del Profesor' }}
      </v-card-title>
      <img alt="Graduation Cap" class="graduation-logo" src="@/assets/graduation.png">
      <v-divider class="my-5" />
      <v-card-text class="pt-0">
        <div v-if="user">
          <v-row dense>
            <v-col cols="12">
              <v-list-item>
                <v-list-item-title class="font-weight-bold">Nombre:</v-list-item-title>
                <v-list-item-subtitle>{{ user.nombre }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            <v-col cols="12">
              <v-list-item>
                <v-list-item-title class="font-weight-bold">DNI:</v-list-item-title>
                <v-list-item-subtitle>{{ user.dni }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            <v-col cols="12">
              <v-list-item>
                <v-list-item-title class="font-weight-bold">Legajo:</v-list-item-title>
                <v-list-item-subtitle>{{ user.legajo || 'N/A' }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
            <v-col cols="12">
              <v-list-item>
                <v-list-item-title class="font-weight-bold">Email:</v-list-item-title>
                <v-list-item-subtitle>{{ user.email || 'N/A' }}</v-list-item-subtitle>
              </v-list-item>
            </v-col>
          </v-row>
        </div>
        <v-alert v-else-if="!loading && !user" text="No se encontraron datos para el profesor." type="warning" />
        <v-alert v-else-if="error" text="Error al cargar los datos del profesor." type="error" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
  import { useAuthUser } from '../../services/user/useAuthUser'

  // Desestructura las propiedades reactivas del servicio useAuthUser
  const { user, loading, error, fetchAuthUser } = useAuthUser()

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(() => {
    fetchAuthUser() // Llama a la función para cargar los datos del usuario
  })
</script>

<style scoped>
/* Estilos para la tarjeta del profesor */
.teacher-card {
  width: 100%; /* Ancho completo */
  max-width: 400px; /* Ancho máximo */
  padding: 10px; /* Relleno interno */
}

/* Estilos para el logo de graduación */
.graduation-logo {
  max-width: 180px; /* Ancho máximo */
  height: auto; /* Altura automática para mantener la proporción */
  display: block; /* Hace que la imagen sea un bloque para centrarla */
  margin: 0 auto 0px auto; /* Centra la imagen horizontalmente */
}
</style>
