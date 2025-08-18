<template>
  <v-autocomplete
    ref="autocompleteRef"
    v-model:search="searchInput"
    autocomplete="off"
    clearable
    :disabled="!careerId"
    :filter-items="false"
    :hide-no-data="true"
    item-title="materia"
    item-value="id"
    :items="subjects"
    :label="label"
    :loading="loading"
    :model-value="modelValue"
    :no-data-text="computedNoDataText"
    variant="outlined"
    @update:model-value="onSubjectSelected"
    @update:search-input="searchInput = $event"
  />
</template>

<script setup>
  import { useSubjectSearch } from '../../services/admin/useSubjectSearch'

  // Define las propiedades que el componente puede recibir
  const props = defineProps({
    // ID de la carrera para filtrar materias
    careerId: [Number, String, null],
    // Valor actual de la materia seleccionada
    modelValue: [Number, String, null],
    // Etiqueta para el campo de autocompletado
    label: {
      type: String,
      default: 'Seleccionar Materia',
    },
  })
  // Define los eventos que el componente puede emitir
  const emit = defineEmits(['update:modelValue'])

  // Obtiene la función para buscar materias por carrera desde el servicio
  const { fetchSubjectsByCareer } = useSubjectSearch()

  // Variables reactivas para el estado del componente
  const subjects = ref([]) // Almacena la lista de materias obtenidas
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
    if (subjects.value.length === 0 && searchInput.value) {
      return 'No se encontraron resultados.'
    }
    return '' // Vacío si no se cumplen las condiciones anteriores
  })

  // Observa cambios en el ID de la carrera y en el input de búsqueda para realizar la búsqueda de materias
  watch([() => props.careerId, searchInput], async ([newCareerId, newSubjectQuery]) => {
    // Limpia el temporizador anterior para evitar múltiples llamadas
    clearTimeout(debounceTimer)

    // Si no hay un ID de carrera, limpia la lista de materias
    if (!newCareerId) {
      loading.value = false
      subjects.value = [] // Siempre vaciamos si no hay carrera
      if (props.modelValue !== null) emit('update:modelValue', null)
      return
    }

    // Elimina espacios en blanco del query de búsqueda
    const trimmedSubjectQuery = newSubjectQuery ? newSubjectQuery.trim() : ''

    let currentlySelectedSubjectObject = null
    // Si hay un valor seleccionado, busca el objeto de la materia correspondiente
    if (props.modelValue !== null) {
      currentlySelectedSubjectObject = subjects.value.find(s => s.id === props.modelValue)
    }

    // Si el query está vacío, o si el query coincide con el nombre de la materia ya seleccionada,
    // se muestra la materia seleccionada o se limpia la lista
    if (!trimmedSubjectQuery || (props.modelValue !== null && currentlySelectedSubjectObject && trimmedSubjectQuery === currentlySelectedSubjectObject.materia)) {
      subjects.value = currentlySelectedSubjectObject ? [currentlySelectedSubjectObject] : []
      loading.value = false
      return
    }

    // Inicia un temporizador para ejecutar la búsqueda después de un retraso (debounce)
    debounceTimer = setTimeout(async () => {
      loading.value = true // Activa el indicador de carga
      try {
        // Llama a la API para obtener las materias que coinciden con el ID de la carrera y el query
        const fetchedSubjects = await fetchSubjectsByCareer(newCareerId, trimmedSubjectQuery)

        if (Array.isArray(fetchedSubjects)) {
          // Mapea las materias para agregar la propiedad 'materia'
          subjects.value = fetchedSubjects.map(s => ({
            ...s,
            materia: s.materia_nombre || '',
          }))
        } else {
          // Muestra una advertencia si la API no devuelve un array
          console.warn('La API no devolvió un array de materias para la carrera:', fetchedSubjects)
          subjects.value = []
        }
      } catch (error) {
        // Maneja errores durante la llamada a la API
        console.error('Error al buscar materias por carrera:', error)
        subjects.value = []
      } finally {
        loading.value = false
      }
    }, 300) // Retraso de 300ms para el debounce
  }, { immediate: true }) // Ejecuta el watcher inmediatamente al montar el componente

  // Maneja la selección de una materia en el autocompletado
  const onSubjectSelected = selectedValue => {
    let idToEmit = null

    // Determina el ID a emitir según el tipo del valor seleccionado
    if (typeof selectedValue === 'number') {
      idToEmit = selectedValue
    } else if (typeof selectedValue === 'string') {
      const foundSubject = subjects.value.find(s => s.materia === selectedValue)
      if (foundSubject) {
        idToEmit = foundSubject.id
      }
    } else if (selectedValue === null) {
      idToEmit = null
    }

    // Emite el evento 'update:modelValue' con el ID de la materia seleccionada
    emit('update:modelValue', idToEmit)

    // Busca la materia seleccionada por su ID
    const selectedSubject = subjects.value.find(s => s.id === idToEmit)
    if (selectedSubject) {
      // Si se seleccionó una materia válida, actualiza el input y la lista de materias
      searchInput.value = selectedSubject.materia
      subjects.value = [selectedSubject]
    } else {
      // Si no se seleccionó una materia (ej. se limpió el campo), resetea el input y la lista
      searchInput.value = ''
      subjects.value = []
    }

    // Si se tiene la referencia al componente, quita el foco del input
    if (autocompleteRef.value) {
      autocompleteRef.value.blur()
    }
  }
</script>

<style scoped>

</style>
