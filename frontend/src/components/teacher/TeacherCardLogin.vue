<template>
  <v-container class="d-flex align-center justify-center" fluid>
    <v-card class="teacher-card">
      <v-card-title class="text-h6 text-center text-wrap mt-4 card-title-custom">
        {{ user ? user.carrera_nombre || 'Detalles del Profesor' : 'Detalles del Profesor' }}
      </v-card-title>
      <v-card-text class="pt-0 fill-height">
        <v-row align="center" justify="center">
          <v-col class="col-border" cols="12" md="6">
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
          </v-col>
          <v-col class="d-flex align-center justify-center col-border" cols="12" md="5">
            <img alt="Graduation Cap" class="graduation-logo" src="@/assets/graduation.png">
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
/* Estilos para la tarjeta del profesor */
.teacher-card {
  max-width: 800px; /* Ancho máximo */
  width: 100%; /* Ocupa el 100% del ancho disponible hasta el max-width */
  padding: 10px; /* Relleno interno */
  display: flex; /* Hace que la tarjeta sea un contenedor flex */
  flex-direction: column; /* Apila los elementos hijos verticalmente */
}

/* Estilos para el logo de graduación */
.graduation-logo {
  max-width: 280px; /* Ancho máximo */
  height: auto; /* Altura automática para mantener la proporción */
  display: block; /* Hace que la imagen sea un bloque para centrarla */
}

/* Estilos para el tamaño de la fuente */
.teacher-card .v-list-item-title {
  font-size: 1rem; /* Aumenta el tamaño de la fuente para los títulos */
}

.teacher-card .v-list-item-subtitle {
  font-size: 1rem; /* Aumenta el tamaño de la fuente para los subtítulos */
  line-height: 1.2; /* Aumenta la altura de línea para más espacio vertical al texto */
}

/* Estilos para el título de la tarjeta personalizado */
.card-title-custom {
  font-size: 1.7rem !important; /* Ajusta el tamaño. !important es necesario para anular estilos de Vuetify. */
  line-height: 1.2; /* Ajusta el interlineado si es necesario */
}

/* Estilos para el contenido de la tarjeta */
.v-card-text.fill-height {
  flex-grow: 1; /* Hace que ocupe el espacio restante */
  display: flex; /* Usa flexbox para que el contenido interno se ajuste */
  flex-direction: column; /* Asegura que los elementos internos se apilen verticalmente */
}
</style>
