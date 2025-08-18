<template>
  <v-autocomplete
    ref="autocompleteRef"
    v-model:search="searchInput"
    autocomplete="off"
    clearable
    :disabled="!careerId"
    :filter-items="false"
    :hide-no-data="true"
    item-title="nombreCompleto"
    item-value="id"
    :items="students"
    :label="label"
    :loading="loading"
    :model-value="modelValue"
    :no-data-text="computedNoDataText"
    variant="outlined"
    @update:model-value="onStudentSelected"
    @update:search-input="searchInput = $event"
  />
</template>

<script setup>
  import { useStudentSearch } from '../../services/student/useStudentSearch'

  // Define las propiedades que el componente puede recibir
  const props = defineProps({
    // ID de la carrera para filtrar estudiantes
    careerId: [Number, String, null],
    // Valor actual del estudiante seleccionado
    modelValue: [Number, String, null],
    // Etiqueta para el campo de autocompletado
    label: {
      type: String,
      default: 'Seleccionar Estudiante',
    },
  })
  // Define los eventos que el componente puede emitir
  const emit = defineEmits(['update:modelValue', 'student-data-selected'])

  // Obtiene la función para buscar estudiantes por carrera desde el servicio
  const { fetchStudentsByCareer } = useStudentSearch()

  // Variables reactivas para el estado del componente
  const students = ref([]) // Almacena la lista de estudiantes obtenidas
  const loading = ref(false) // Indicador de carga
  const searchInput = ref('') // Valor del input de búsqueda
  let debounceTimer = null // Temporizador para el debounce de la búsqueda
  const autocompleteRef = ref(null) // Referencia al componente v-autocomplete

  // Propiedad computada para el texto de "sin datos" en el autocompletado
  const computedNoDataText = computed(() => {
    // Si no se ha seleccionado una carrera, muestra un mensaje
    if (!props.careerId) {
      return 'Seleccione una carrera primero.'
    }
    // Si está cargando, muestra un mensaje de carga
    if (loading.value) {
      return 'Cargando...'
    }
    // Si no hay resultados y hay texto de búsqueda, muestra un mensaje de "no se encontraron resultados"
    if (students.value.length === 0 && searchInput.value) {
      return 'No se encontraron resultados.'
    }
    return '' // Vacío si no se cumplen las condiciones anteriores
  })

  // Observa cambios en el ID de la carrera y en el input de búsqueda para realizar la búsqueda de estudiantes
  watch([() => props.careerId, searchInput], async ([newCareerId, newStudentQuery]) => {
    // Limpia el temporizador anterior para evitar múltiples llamadas
    clearTimeout(debounceTimer)

    // Si no hay un ID de carrera, limpia la lista de estudiantes y el valor seleccionado
    if (!newCareerId) {
      loading.value = false
      students.value = []
      if (props.modelValue !== null) emit('update:modelValue', null)
      return
    }

    // Elimina espacios en blanco del query de búsqueda
    const trimmedStudentQuery = newStudentQuery ? newStudentQuery.trim() : ''

    let currentlySelectedStudentObject = null
    // Si hay un valor seleccionado, busca el objeto del estudiante correspondiente
    if (props.modelValue !== null) {
      currentlySelectedStudentObject = students.value.find(s => s.id === props.modelValue)
    }

    // Si el query está vacío, o si el query coincide con el nombre del estudiante ya seleccionado,
    // se muestra el estudiante seleccionado o se limpia la lista
    if (!trimmedStudentQuery || (props.modelValue !== null && currentlySelectedStudentObject && trimmedStudentQuery === currentlySelectedStudentObject.nombreCompleto)) {
      students.value = currentlySelectedStudentObject ? [currentlySelectedStudentObject] : []
      loading.value = false
      return
    }

    // Inicia un temporizador para ejecutar la búsqueda después de un retraso (debounce)
    debounceTimer = setTimeout(async () => {
      loading.value = true // Activa el indicador de carga
      try {
        // Llama a la API para obtener los estudiantes que coinciden con el ID de la carrera y el query
        const fetchedStudents = await fetchStudentsByCareer(newCareerId, trimmedStudentQuery)

        if (Array.isArray(fetchedStudents)) {
          // Mapea los estudiantes para agregar la propiedad 'nombreCompleto'
          students.value = fetchedStudents.map(s => ({
            ...s,
            nombreCompleto: s.nombre || '',
          }))
        } else {
          // Muestra una advertencia si la API no devuelve un array
          console.warn('La API no devolvió un array de estudiantes para la carrera:', fetchedStudents)
          students.value = [] // Limpia la lista si la respuesta no es un array
        }
      } catch (error) {
        // Maneja errores durante la llamada a la API
        console.error('Error al buscar estudiantes por carrera:', error)
        students.value = [] // Limpia la lista en caso de error
      } finally {
        loading.value = false // Desactiva el indicador de carga
      }
    }, 300) // Retraso de 300ms para el debounce
  }, { immediate: true }) // Ejecuta el watcher inmediatamente al montar el componente

  // Maneja la selección de un estudiante en el autocompletado
  const onStudentSelected = selectedId => {
    // Encuentra el objeto del estudiante seleccionado por su ID
    const selectedStudent = students.value.find(s => s.id === selectedId)

    // Emite el evento 'update:modelValue' con el ID del estudiante seleccionado
    emit('update:modelValue', selectedId)

    if (selectedStudent) {
      // Emite el evento 'student-data-selected' con los datos del estudiante seleccionado
      emit('student-data-selected', selectedStudent)
      // Si se seleccionó un estudiante válido, actualiza el input y la lista de estudiantes
      searchInput.value = selectedStudent.nombreCompleto
      students.value = [selectedStudent]
    } else {
      // Si no se seleccionó un estudiante (ej. se limpió el campo), resetea el input y la lista
      searchInput.value = ''
      students.value = []
    }

    // Si se tiene la referencia al componente, quita el foco del input
    if (autocompleteRef.value) {
      autocompleteRef.value.blur()
    }
  }
</script>

<style scoped>

</style>
