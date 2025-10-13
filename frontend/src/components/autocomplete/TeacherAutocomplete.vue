<template>
  <v-autocomplete
    ref="autocompleteRef"
    v-model:search="searchInput"
    autocomplete="off"
    clearable
    :disabled="!careerId"
    :filter-items="false"
    hide-details="auto"
    :hide-no-data="true"
    item-title="nombre"
    item-value="id"
    :items="professors"
    :label="label"
    :loading="loading"
    :model-value="modelValue"
    :no-data-text="computedNoDataText"
    variant="solo-inverted"
    @update:model-value="onProfessorSelected"
    @update:search-input="searchInput = $event"
  />
</template>

<script setup>
  import { useTeacherSearch } from '../../services/teacher/useTeacherSearch'

  // Define las propiedades que el componente puede recibir
  const props = defineProps({
    // ID de la carrera para filtrar profesores
    careerId: [Number, String, null],
    // Valor actual del profesor seleccionado
    modelValue: [Number, String, null],
    // Etiqueta para el campo de autocompletado
    label: {
      type: String,
      default: 'Seleccionar Profesor',
    },
  })
  // Define los eventos que el componente puede emitir
  const emit = defineEmits(['update:modelValue', 'teacher-data-selected'])

  // Obtiene la función para buscar profesores por carrera desde el servicio
  const { fetchTeachersByCareer } = useTeacherSearch()

  // Variables reactivas para el estado del componente
  const professors = ref([]) // Almacena la lista de profesores obtenidas
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
    if (professors.value.length === 0 && searchInput.value) {
      return 'No se encontraron resultados.'
    }
    return '' // Vacío si no se cumplen las condiciones anteriores
  })

  // Observa cambios en el ID de la carrera y en el input de búsqueda para realizar la búsqueda de profesores
  watch([() => props.careerId, searchInput], async ([newCareerId, newProfessorQuery]) => {
    // Limpia el temporizador anterior para evitar múltiples llamadas
    clearTimeout(debounceTimer)

    // Si no hay un ID de carrera, limpia la lista de profesores
    if (!newCareerId) {
      loading.value = false
      professors.value = []
      if (props.modelValue !== null) emit('update:modelValue', null)
      return
    }

    // Elimina espacios en blanco del query de búsqueda
    const trimmedProfessorQuery = newProfessorQuery ? newProfessorQuery.trim() : ''

    let currentlySelectedProfessorObject = null
    // Si hay un valor seleccionado, busca el objeto del profesor correspondiente
    if (props.modelValue !== null) {
      currentlySelectedProfessorObject = professors.value.find(p => p.id === props.modelValue)
    }

    // Si el query está vacío, o si el query coincide con el nombre del profesor ya seleccionado,
    // se muestra el profesor seleccionado o se limpia la lista
    if (!trimmedProfessorQuery || (props.modelValue !== null && currentlySelectedProfessorObject && trimmedProfessorQuery === currentlySelectedProfessorObject.nombre)) {
      professors.value = currentlySelectedProfessorObject ? [currentlySelectedProfessorObject] : []
      loading.value = false
      return
    }

    // Inicia un temporizador para ejecutar la búsqueda después de un retraso (debounce)
    debounceTimer = setTimeout(async () => {
      loading.value = true // Activa el indicador de carga
      try {
        // Llama a la API para obtener los profesores que coinciden con el ID de la carrera y el query
        const fetchedProfessors = await fetchTeachersByCareer(newCareerId, trimmedProfessorQuery)

        if (Array.isArray(fetchedProfessors)) {
          // Mapea los profesores para agregar la propiedad 'nombre'
          professors.value = fetchedProfessors.map(p => ({
            ...p,
            nombre: p.nombre || '',
          }))
        } else {
          // Muestra una advertencia si la API no devuelve un array
          console.warn('La API no devolvió un array de profesores para la carrera:', fetchedProfessors)
          professors.value = []
        }
      } catch (error) {
        // Maneja errores durante la llamada a la API
        console.error('Error al buscar profesores por carrera:', error)
        professors.value = []
      } finally {
        loading.value = false
      }
    }, 300) // Retraso de 300ms para el debounce
  }, { immediate: true }) // Ejecuta el watcher inmediatamente al montar el componente

  // Maneja la selección de un profesor en el autocompletado
  const onProfessorSelected = selectedId => {
    // Busca el profesor seleccionado por su ID
    const selectedProfessor = professors.value.find(p => p.id === selectedId)

    // Emite el evento 'update:modelValue' con el ID del profesor seleccionado
    emit('update:modelValue', selectedId)

    if (selectedProfessor) {
      // Si se seleccionó un profesor válido, actualiza el input y la lista de profesores
      searchInput.value = selectedProfessor.nombre
      professors.value = [selectedProfessor]
      emit('teacher-data-selected', selectedProfessor)
    } else {
      // Si no se seleccionó un profesor (ej. se limpió el campo), resetea el input y la lista
      searchInput.value = ''
      professors.value = []
    }

    // Si se tiene la referencia al componente, quita el foco del input
    if (autocompleteRef.value) {
      autocompleteRef.value.blur()
    }
  }
</script>

<style scoped>

</style>
