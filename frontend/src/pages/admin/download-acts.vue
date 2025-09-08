<template>
  <v-card class="pa-4" width="1000">
    <v-card class="mb-4 no-card-styles">
      <v-card-title class="centered-title">Actas Digitales</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="searchQuery"
              clearable
              hide-details
              label="Nombre del Profesor"
              @keyup.enter="searchActs"
            />
          </v-col>
          <v-col cols="12">
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
      </v-card-text>
    </v-card>

    <v-card class="mt-4">
      <v-card-text>
        <v-alert v-if="error" class="mb-4" type="error">{{ error }}</v-alert>
        <v-alert v-if="!loading && actas.length === 0 && searchQuery" class="mb-4" type="info">
          No se encontraron actas para el profesor "{{ searchQuery }}".
        </v-alert>
        <v-data-table
          :headers="headers"
          hide-default-footer
          item-value="id"
          :items="actas"
          :loading="loading"
          loading-text="Cargando actas..."
          no-data-text="Realiza una búsqueda para ver las actas."
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
  </v-card>
</template>

<script setup>
  import { ref } from 'vue'
  import { useDigitalActsDownload } from '@/services/admin/useDigitalActsDownload'
  import { useDigitalActsUploader } from '@/services/admin/useDigitalActsUploader'

  const { fetchPdfsByUploaderName } = useDigitalActsUploader()
  const { downloadPdfById } = useDigitalActsDownload()

  const searchQuery = ref('')
  const actas = ref([])
  const loading = ref(false)
  const error = ref(null)

  const headers = [
    { title: 'Nombre de Archivo', key: 'filename' },
    { title: 'Fecha de Subida', key: 'upload_date' },
    { title: 'Subido por', key: 'uploaded_by_name' },
    { title: 'Acción', key: 'action', sortable: false },
  ]

  const searchActs = async () => {
    error.value = null
    if (!searchQuery.value) {
      actas.value = []
      return
    }

    loading.value = true
    try {
      const result = await fetchPdfsByUploaderName(searchQuery.value)
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
}
.v-data-table {
  background-color: transparent !important;
}
</style>

<route lang="yaml">
  meta:
    layout: admin
</route>
