<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="12" md="7">
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
          </v-col>
          <v-col class="d-flex align-center justify-center" cols="12" md="5">
            <img
              alt="Birrete"
              src="@/assets/birrete_logo_280px.webp"
            >
          </v-col>
        </v-row>
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
/* Estilos para sobreescribir el .v-card */
.v-card {
  border: none !important;
  max-width: 750px; /* Ancho máximo */
  background: linear-gradient(to right, #ffffff) !important;
}

/* Estilos para el título de la tarjeta personalizado */
.v-card-title {
  font-size: 1.7rem !important; /* Ajusta el tamaño. !important es necesario para anular estilos de Vuetify. */
  line-height: 1.2; /* Ajusta el interlineado si es necesario */
  color: black !important;
}

.v-list-item-subtitle {
  font-size: 1rem; /* Aumenta el tamaño de la fuente para los subtítulos */
  line-height: 1.2; /* Aumenta la altura de línea para más espacio vertical al texto */
  color: black !important;
}

/* Estilos para el tamaño de la fuente */
.v-list-item-title {
  font-size: 1rem; /* Aumenta el tamaño de la fuente para los títulos */
  color: black !important;
}

/* Estilos para los alerts */
.v-alert {
  color: black !important;
}
</style>
