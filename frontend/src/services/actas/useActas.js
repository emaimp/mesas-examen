import { api } from '@/services/api';

export function useActas() {
  const getMateriasProfesor = async (idProfesor) => {
    try {
      const response = await api.get(`/profesores/${idProfesor}/materias`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener las materias del profesor:', error);
      throw error;
    }
  };

  const getMesasExamen = async (idMateria) => {
    try {
      const response = await api.get(`/materias/${idMateria}/mesas`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener las mesas de examen:', error);
      throw error;
    }
  };

  const getAlumnosInscriptos = async (idMesa) => {
    try {
      const response = await api.get(`/mesas-examen/${idMesa}/alumnos`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener los alumnos inscriptos:', error);
      throw error;
    }
  };

  return {
    getMateriasProfesor,
    getMesasExamen,
    getAlumnosInscriptos,
  };
}