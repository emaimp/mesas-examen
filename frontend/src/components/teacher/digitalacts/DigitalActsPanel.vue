<template>
  <v-card style="position: relative;" width="750">
    <v-card style="padding-bottom: 50px;">
      <v-card-title class="text-center mb-2 mt-3">Acta Digital</v-card-title>
      <v-card-text>
        <v-alert
          v-if="loading"
          class="mb-4"
          text="Cargando actas..."
          type="info"
          variant="tonal"
        />
        <v-alert
          v-else-if="error"
          class="mb-4"
          :text="`Error al cargar las actas: ${error.message}`"
          type="error"
          variant="tonal"
        />
        <v-alert
          v-else-if="!detailExams || detailExams.length === 0"
          class="mb-4"
          text="No hay actas registradas."
          type="info"
          variant="tonal"
        />
        <div v-else>
          <div id="digital-acts-content">
            <v-card
              v-for="carreraData in groupedDigitalActs"
              :key="carreraData.carrera_nombre"
              class="pa-5"
              flat
            >
              <v-card-title class="text-wrap text-subtitle-1">
                {{ carreraData.carrera_nombre }}
              </v-card-title>
              <v-card-subtitle class="pt-0 pb-2">
                Materia: {{ carreraData.mesas[0]?.materia_nombre || 'No disponible' }}
              </v-card-subtitle>
              <v-card-subtitle class="pt-0 pb-5">
                Profesor: {{ profesorName }}
              </v-card-subtitle>
              <v-row>
                <v-col>
                  <v-text-field
                    v-model="careerObservations[carreraData.carrera_nombre]"
                    class="mb-2"
                    dense
                    hide-details="auto"
                    label="Observaciones"
                    outlined
                    persistent-placeholder
                    style="color: #000000;"
                  />
                </v-col>
              </v-row>
              <v-card-text>
                <v-row>
                  <v-col
                    v-for="digitalAct in carreraData.mesas.filter(mesa => mesa.estado === 'active')"
                    :key="digitalAct.id_inscripcion"
                    class="ma-0 pa-0"
                    cols="12"
                  >
                    <DigitalActsCard :digital-act="digitalAct" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div> <!-- Cierre del contenedor de la acta -->
        </div>
      </v-card-text>
    </v-card>
    <div class="pdf-export-button-container">
      <v-btn
        class="action-button"
        :disabled="uploadLoading"
        @click="exportToPDF"
      >
        <span v-if="uploadLoading">Subiendo PDF...</span>
        <span v-else>Exportar Actas</span>
      </v-btn>
    </div>
  </v-card>
</template>

<script setup>
  import html2pdf from 'html2pdf.js'
  import { useDetailExam } from '@/services/teacher/useDetailExam.js'
  import { useDigitalActsService } from '@/services/teacher/useDigitalActs.js'
  import { useAuthUser } from '@/services/user/useAuthUser.js'
  import DigitalActsCard from './DigitalActsCard.vue'

  // Estado para la autenticación del usuario
  const { user, loading: authLoading, error: authError, fetchAuthUser } = useAuthUser()
  const profesorId = ref(null)
  const profesorName = ref('')

  // Estado para los detalles del examen
  const { detailExams, loading: detailExamsLoading, error: detailExamsError, fetchDetailExams } = useDetailExam()

  // Estado para las observaciones generales por carrera
  const careerObservations = ref({})

  // Propiedad computada para agrupar actas digitales por carrera_nombre
  const groupedDigitalActs = computed(() => {
    if (!detailExams.value || detailExams.value.length === 0) {
      return []
    }
    // La API de detailExams ya devuelve los datos agrupados por carrera_nombre
    return detailExams.value
  })

  // Observar cambios en groupedDigitalActs para inicializar careerObservations
  watch(groupedDigitalActs, newGroupedActs => {
    for (const carreraData of newGroupedActs) {
      if (!(carreraData.carrera_nombre in careerObservations.value)) {
        careerObservations.value[carreraData.carrera_nombre] = 'Sin observaciones'
      }
    }
  }, { immediate: true, deep: true })

  // Hook de ciclo de vida para obtener datos cuando el componente es montado
  onMounted(() => {
    fetchAuthUser()
  })

  // Observar cambios en el usuario autenticado
  watch(user, newUser => {
    if (newUser) {
      profesorName.value = newUser.nombre || 'Nombre no disponible'
      profesorId.value = newUser.id
      if (profesorId.value) {
        fetchDetailExams(profesorId.value)
      }
    } else {
      profesorName.value = ''
      profesorId.value = null
    }
  })

  // Estados combinados de carga y error
  const loading = computed(() => authLoading.value || detailExamsLoading.value)
  const error = computed(() => authError.value || detailExamsError.value)

  // Usar el nuevo servicio para subir PDFs
  const { uploadDigitalActPdf, loading: uploadLoading, error: uploadError } = useDigitalActsService()

  // Función para exportar a PDF
  const exportToPDF = async () => {
    const element = document.querySelector('#digital-acts-content')
    if (element) {
      try {
        const pdfBlob = await html2pdf().from(element).outputPdf('blob')
        const filename = 'actas_digitales.pdf'

        const result = await uploadDigitalActPdf(pdfBlob, filename)

        if (result) {
          console.log('PDF subido exitosamente:', result)
          alert('Actas digitales subidas exitosamente.')
        } else {
          console.error('Error al subir el PDF:', uploadError.value)
          alert(`Error al subir el PDF: ${uploadError.value?.message || 'Error desconocido'}`)
        }
      } catch (error_) {
        console.error('Error al generar o subir el PDF:', error_)
        alert('Ocurrió un error al generar o subir el PDF.')
      }
    } else {
      console.error('No se encontró el elemento para exportar a PDF.')
      alert('No se encontró el contenido para exportar a PDF.')
    }
  }
</script>

<style scoped>
.v-card {
  border: none !important;
  background: #ffffff !important;
}

#digital-acts-content .v-card {
  box-shadow: none !important;
}

.pdf-export-button-container {
  position: absolute;
  bottom: 16px;
  right: 16px;
}

.v-card-title,
.v-card-subtitle,
.v-card-text {
  color: #000000 !important;
}
</style>
