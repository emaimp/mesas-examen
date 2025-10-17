<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="7" sm="10">

        <v-row>
          <v-col cols="12">
            <v-card>
              <v-card-text class="pt-8">
                <v-row class="mb-8" justify="center">
                  <v-col cols="12" md="8" sm="10">
                    <TeacherAutocomplete
                      v-model="selectedTeacherId"
                      use-global-search
                      label="Seleccionar Profesor"
                      @teacher-data-selected="onTeacherSelected"
                    />
                  </v-col>
                  <v-col cols="12" md="5" sm="10">
                    <v-btn
                      block
                      class="action-button"
                      :loading="loading"
                      @click="searchActs"
                    >
                      <v-icon left>mdi-magnify</v-icon>
                      Buscar Actas
                    </v-btn>
                  </v-col>
                </v-row>
                <v-divider class="my-1" />
                <v-alert v-if="error" class="mb-4" type="error">{{ error }}</v-alert>
                <v-data-table
                  :headers="headers"
                  hide-default-footer
                  item-value="id"
                  :items="actas"
                  :loading="loading"
                  loading-text="Cargando actas..."
                  no-data-text="Realiza una búsqueda."
                >
                  <template #item.upload_date="{ item }">
                    {{ new Date(item.upload_date).toLocaleDateString() }}
                  </template>
                  <template #item.action="{ item }">
                    <v-btn
                      class="action-button"
                      size="small"
                      variant="outlined"
                      @click="descargarActa(item)"
                    >
                      <v-icon left>mdi-download</v-icon>
                      Descargar
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import TeacherAutocomplete from '@/components/autocomplete/TeacherAutocomplete.vue'
  import { useDigitalActsDownload } from '@/services/admin/useDigitalActsDownload'
  import { useDigitalActsUploader } from '@/services/admin/useDigitalActsUploader'

  const { fetchPdfsByUploaderName } = useDigitalActsUploader()
  const { downloadPdfById } = useDigitalActsDownload()

  const selectedTeacherId = ref(null)
  const selectedTeacherData = ref(null)
  const actas = ref([])
  const loading = ref(false)
  const error = ref(null)
  const hasSearched = ref(false)

  const headers = [
    { title: 'Nombre de Archivo', key: 'filename' },
    { title: 'Fecha de Subida', key: 'upload_date' },
    { title: 'Profesor', key: 'uploaded_by_name' },
    { title: 'Acción', key: 'action', sortable: false },
  ]

  const onTeacherSelected = teacherData => {
    selectedTeacherData.value = teacherData
  }

  const searchActs = async () => {
    error.value = null
    hasSearched.value = true

    // Si no hay profesor seleccionado ni datos, no hacer nada
    if (!selectedTeacherId.value && !selectedTeacherData.value) {
      actas.value = []
      return
    }

    loading.value = true
    try {
      // Usar el nombre del profesor seleccionado para la búsqueda
      const teacherName = selectedTeacherData.value?.nombre || ''
      const result = await fetchPdfsByUploaderName(teacherName)
      actas.value = result
    } catch (error_) {
      error.value = error_.message || 'Error al buscar actas.'
      actas.value = []
    } finally {
      loading.value = false
    }
  }

  const descargarActa = async item => {
    try {
      await downloadPdfById(item.id, item.filename)
    } catch (error_) {
      console.error('Error al descargar el acta:', error_.message)
      // Aquí podrías mostrar un snackbar o alerta al usuario
    }
  }
</script>

<style scoped>
.centered-title {
  text-align: center;
  margin-bottom: 20px;
}
.no-card-styles {
  border: none !important;
  box-shadow: none !important;
  background: none !important; /* Using 'background: none' for a more comprehensive removal */
}
.centered-card {
  margin: 0 auto;
}
.v-data-table {
  background-color: transparent !important;
}
</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
