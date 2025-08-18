<template>
  <v-autocomplete
    ref="autocompleteRef"
    v-model:search="searchInput"
    autocomplete="off"
    clearable
    :filter-items="false"
    :hide-no-data="true"
    item-title="nombre"
    item-value="id"
    :items="careers"
    :label="label"
    :loading="loading"
    :model-value="modelValue"
    :no-data-text="computedCareerNoDataText"
    variant="outlined"
    @update:model-value="onCareerSelected"
    @update:search-input="searchInput = $event"
  />
</template>

<script setup>
  import { useCareerSearch } from '../../services/admin/useCareerSearch'

  // Define las propiedades que el componente puede recibir
  const props = defineProps({
    // Valor actual de la carrera seleccionada (puede ser número o string, o nulo)
    modelValue: [Number, String, null],
    // Etiqueta para el campo de autocompletado
    label: {
      type: String,
      default: 'Buscar Carrera', // Valor por defecto si no se proporciona
    },
  })
  // Define los eventos que el componente puede emitir
  const emit = defineEmits(['update:modelValue'])

  // Obtiene la función para buscar carreras desde el servicio
  const { fetchCareers } = useCareerSearch()

  // Variables reactivas para el estado del componente
  const careers = ref([]) // Almacena la lista de carreras obtenidas
  const loading = ref(false) // Indicador de carga
  const searchInput = ref('') // Valor del input de búsqueda
  let debounceTimer = null // Temporizador para el debounce de la búsqueda
  const autocompleteRef = ref(null) // Referencia al componente v-autocomplete

  // Propiedad computada para el texto de "sin datos" en el autocompletado
  const computedCareerNoDataText = computed(() => {
    if (loading.value) {
      return 'Cargando...' // Muestra "Cargando..." si está buscando
    }
    if (careers.value.length === 0 && searchInput.value) {
      return 'No se encontraron resultados.' // Muestra mensaje si no hay resultados y hay texto de búsqueda
    }
    return '' // Vacío si no se cumplen las condiciones anteriores
  })

  // Observa cambios en el input de búsqueda para realizar la búsqueda de carreras
  watch(searchInput, async newQuery => {
    // Limpia el temporizador anterior para evitar múltiples llamadas
    clearTimeout(debounceTimer)

    // Elimina espacios en blanco del query de búsqueda
    const trimmedQuery = newQuery ? newQuery.trim() : ''

    let currentlySelectedCareerObject = null
    // Si hay un valor seleccionado, busca el objeto de la carrera correspondiente
    if (props.modelValue !== null) {
      currentlySelectedCareerObject = careers.value.find(c => c.id === props.modelValue)
    }

    // Si el query está vacío, o si el query coincide con el nombre de la carrera ya seleccionada,
    // se muestra la carrera seleccionada o se limpia la lista
    if (!trimmedQuery || (props.modelValue !== null && currentlySelectedCareerObject && trimmedQuery === currentlySelectedCareerObject.nombre)) {
      careers.value = currentlySelectedCareerObject ? [currentlySelectedCareerObject] : []
      loading.value = false
      return
    }

    // Inicia un temporizador para ejecutar la búsqueda después de un retraso (debounce)
    debounceTimer = setTimeout(async () => {
      loading.value = true // Activa el indicador de carga
      try {
        // Llama a la API para obtener las carreras que coinciden con el query
        const fetchedCareers = await fetchCareers(trimmedQuery)
        if (Array.isArray(fetchedCareers)) {
          careers.value = fetchedCareers // Actualiza la lista de carreras
        } else {
          // Muestra una advertencia si la API no devuelve un array
          console.warn('La API no devolvió un array de carreras:', fetchedCareers)
          careers.value = [] // Limpia la lista si la respuesta no es un array
        }
      } catch (error) {
        // Maneja errores durante la llamada a la API
        console.error('Error al buscar carreras:', error)
        careers.value = [] // Limpia la lista en caso de error
      } finally {
        loading.value = false // Desactiva el indicador de carga
      }
    }, 300) // Retraso de 300ms para el debounce
  }, { immediate: true }) // Ejecuta el watcher inmediatamente al montar el componente

  // Maneja la selección de una carrera en el autocompletado
  const onCareerSelected = selectedId => {
    // Encuentra el objeto de la carrera seleccionada por su ID
    const selectedCareer = careers.value.find(c => c.id === selectedId)

    // Emite el evento 'update:modelValue' con el ID de la carrera seleccionada
    emit('update:modelValue', selectedId)

    if (selectedCareer) {
      // Si se seleccionó una carrera válida, actualiza el input y la lista de carreras
      searchInput.value = selectedCareer.nombre
      careers.value = [selectedCareer]
    } else {
      // Si no se seleccionó una carrera (ej. se limpió el campo), resetea el input y la lista
      searchInput.value = ''
      careers.value = []
    }

    // Si se tiene la referencia al componente, quita el foco del input
    if (autocompleteRef.value) {
      autocompleteRef.value.blur()
    }
  }
</script>

<style scoped>

</style>
