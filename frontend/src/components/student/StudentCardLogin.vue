<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card>
      <v-card-text>
        <div class="d-flex flex-column align-center pt-12 px-6">
          <img
            alt="Academic User"
            src="@/assets/student_logo_200px.webp"
            class="mb-13"
          >
          <div v-if="user">
            <v-row>
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
                  <v-list-item-title class="font-weight-bold">Libreta:</v-list-item-title>
                  <v-list-item-subtitle>{{ user.libreta || 'N/A' }}</v-list-item-subtitle>
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
          <v-alert v-else-if="!loading && !user" text="No se encontraron datos para el estudiante." type="warning" />
          <v-alert v-else-if="error" text="Error al cargar los datos del estudiante." type="error" />
        </div>
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
/* Estilos para el v-card */
.v-card {
  height: 680px; /* Alto máximo */
  max-width: 600px; /* Ancho máximo */
}

/* Estilos para el título */
.v-card-title {
  font-size: 1.7rem !important; /* Ajusta el tamaño. !important es necesario para anular estilos de Vuetify. */
  line-height: 1.2; /* Ajusta el interlineado si es necesario */
}

.v-list-item-subtitle {
  font-size: 1rem; /* Aumenta el tamaño de la fuente para los subtítulos */
  line-height: 1.2; /* Aumenta la altura de línea para más espacio vertical al texto */
}

/* Estilos para la fuente */
.v-list-item-title {
  font-size: 1rem; /* Aumenta el tamaño de la fuente para los títulos */
}

/* Estilos del v-list-item */
.v-list-item {
  background-image: repeating-linear-gradient(-45deg, transparent, transparent 10px, rgba(128,128,128,0.1) 10px, rgba(128,128,128,0.1) 11px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 8px;
}
</style>
