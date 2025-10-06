# Convierte el directorio 'r_perfomance' en un paquete de Python

from .porcentaje_inscripciones import porcentaje_inscripciones_carrera
from .prediccion_rendimiento import prediccion_rendimiento_carrera
from .promedio_notas_materias import promedio_notas_materias_carrera
from .rendimiento_demografico import rendimiento_demografico_carrera
from .rendimiento_mesas_examen import rendimiento_mesas_examen_carrera
from .rendimiento_promedio import rendimiento_promedio_carrera

__all__ = [
    'porcentaje_inscripciones_carrera',
    'prediccion_rendimiento_carrera',
    'promedio_notas_materias_carrera',
    'rendimiento_demografico_carrera',
    'rendimiento_mesas_examen_carrera',
    'rendimiento_promedio_carrera',
    ]
