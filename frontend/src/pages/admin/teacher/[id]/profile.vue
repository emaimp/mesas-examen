<template>
  <v-container class="fill-height gradient-background py-9" fluid>
    <v-row align="center" class="fill-height" justify="center">
      <v-col
        cols="12"
        lg="9"
        md="9"
        sm="9"
        xl="9"
      >
        <v-card class="mx-auto pa-7 transparent-card" flat :loading="loading">
          <TeacherCard v-if="teacherId" :teacher-id="teacherId" />
          <v-card-text>
            <div v-if="loading" class="text-center py-5">
              <v-progress-circular color="primary" indeterminate />
              <p class="mt-2 text-white">Cargando datos del profesor...</p>
            </div>
            <v-alert
              v-else-if="!teacherId"
              class="mb-4"
              text="ID del profesor no encontrado en la ruta."
              type="info"
              variant="tonal"
            />
            <v-alert
              v-else-if="!teacher"
              class="mb-4"
              text="No se encontraron datos para el profesor."
              type="warning"
              variant="tonal"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import TeacherCard from '../../../../components/admin/teacher/TeacherCardAdmin.vue'
  import { useTeacherSearch } from '../../../../services/teacher/useTeacherSearch'

  // Obtiene la ruta actual
  const route = useRoute()
  // Inicializa el servicio de búsqueda de profesores
  const { fetchTeacherById } = useTeacherSearch()

  // Estados reactivos para los datos del profesor
  const teacherId = ref(null) // ID del profesor obtenido de la ruta
  const teacher = ref(null) // Datos completos del profesor
  const loading = ref(true) // Indica si los datos están cargando

  // Hook de ciclo de vida: se ejecuta cuando el componente se monta
  onMounted(async () => {
    teacherId.value = route.params.id // Obtiene el ID del profesor de los parámetros de la ruta

    if (teacherId.value) {
      loading.value = true // Activa el estado de carga
      try {
        // Intenta obtener los datos del profesor por su ID
        teacher.value = await fetchTeacherById(teacherId.value)
        if (!teacher.value) {
          console.warn(
            'Datos del profesor no encontrados para el ID:',
            teacherId.value,
          )
        }
      } catch (error) {
        console.error(
          'Error al cargar datos básicos del profesor:',
          error,
        )
        teacher.value = null
      } finally {
        loading.value = false // Desactiva el estado de carga
      }
    } else {
      loading.value = false // Desactiva la carga si no hay ID de profesor
      console.warn(
        'ID del profesor no encontrado en los parámetros de la ruta.',
      )
    }
  })
</script>

<style scoped>

</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
