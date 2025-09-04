<template>
  <v-container>
    <h1 class="mb-4">Gestión de Actas Digitales</h1>

    <v-row>
      <v-col cols="12" md="6">
        <v-select
          label="Seleccionar Materia"
          :items="materias"
          item-title="nombre"
          item-value="id"
          v-model="selectedMateria"
          variant="outlined"
          clearable
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          label="Seleccionar Mesa de Examen"
          :items="mesasExamen"
          item-title="fecha"
          item-value="id"
          v-model="selectedMesa"
          variant="outlined"
          clearable
          :disabled="!selectedMateria"
        />
      </v-col>
    </v-row>

    <v-row v-if="selectedMesa">
      <v-col cols="12">
        <v-card class="mt-4">
          <v-card-title>Alumnos Inscriptos</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="alumnosInscriptos"
              item-value="id"
              class="elevation-1"
            >
              <template v-slot:item.calificacion="{ item }">
                <v-text-field
                  v-model="item.calificacion"
                  type="number"
                  min="1"
                  max="10"
                  density="compact"
                  variant="outlined"
                  hide-details
                />
              </template>
            </v-data-table>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn color="primary" @click="guardarCalificaciones">
              Guardar Calificaciones
            </v-btn>
            <v-btn color="success" @click="generarActa">
              Generar Acta Digital
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAuthUser } from '@/services/user/useAuthUser';
import { useActas } from '@/services/actas/useActas';

const { user } = useAuthUser();
const { getMateriasProfesor, getMesasExamen, getAlumnosInscriptos } = useActas();

const materias = ref([]);
const selectedMateria = ref(null);

const mesasExamen = ref([]);
const selectedMesa = ref(null);

const alumnosInscriptos = ref([]);

const headers = [
  { title: 'Nombre del Alumno', key: 'nombre' },
  { title: 'Calificación', key: 'calificacion', sortable: false },
];

// Lógica para manejar las acciones
const guardarCalificaciones = () => {
  console.log('Guardando calificaciones:', alumnosInscriptos.value);
  // Aquí irá la lógica para enviar al backend
};

const generarActa = () => {
  console.log('Generando acta digital...');
  // Aquí irá la lógica para generar el PDF
};

// Lógica para obtener datos del backend
const fetchMaterias = async () => {
  if (user.value && user.value.id) {
    try {
      materias.value = await getMateriasProfesor(user.value.id);
    } catch (error) {
      console.error('No se pudieron cargar las materias.');
    }
  }
};

const fetchMesasExamen = async () => {
  if (selectedMateria.value) {
    try {
      mesasExamen.value = await getMesasExamen(selectedMateria.value);
    } catch (error) {
      console.error('No se pudieron cargar las mesas de examen.');
    }
  } else {
    mesasExamen.value = [];
  }
};

const fetchAlumnosInscriptos = async () => {
  if (selectedMesa.value) {
    try {
      const data = await getAlumnosInscriptos(selectedMesa.value);
      alumnosInscriptos.value = data.map(alumno => ({ ...alumno, calificacion: null }));
    } catch (error) {
      console.error('No se pudieron cargar los alumnos inscriptos.');
    }
  } else {
    alumnosInscriptos.value = [];
  }
};

// Observadores para reaccionar a los cambios
watch(selectedMateria, fetchMesasExamen);
watch(selectedMesa, fetchAlumnosInscriptos);

// Cargar las materias al montar el componente
onMounted(fetchMaterias);
</script>

<style scoped>
/* Puedes añadir estilos específicos para esta página si es necesario */
</style>

---

### Instrucciones

1.  **Crea el archivo `frontend/src/services/actas/useActas.js`** con el código que te proporcioné.
2.  **Abre `frontend/src/pages/teacher/digital-acts.vue`**.
3.  **Reemplaza todo el contenido** con el código modificado que te acabo de dar.
4.  **Guarda ambos archivos.**
5.  **Reinicia el servidor de desarrollo (`Ctrl + C`, `npm run dev`)**.

El código ahora se encargará de hacer llamadas a las rutas de tu backend que están especificadas en el servicio. Si tu backend aún no tiene esas rutas, te dará errores 404. Si te da errores, no te preocupes, el siguiente paso será crear esas rutas en tu backend.

Avísame cuando hayas completado estos pasos.