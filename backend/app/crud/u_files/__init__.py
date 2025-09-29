# Convierte el directorio 'u_files' en un paquete de Python

from .plan_estudio import cargar_plan_estudio_excel
from .notas import cargar_notas_excel
from .usuarios import cargar_usuarios_excel

__all__ = [
    'cargar_plan_estudio_excel',
    'cargar_notas_excel',
    'cargar_usuarios_excel'
    ]
