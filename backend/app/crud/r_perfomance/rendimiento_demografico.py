from typing import Dict
from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select

#
# Obtiene el rendimiento demográfico de una carrera (género, edad, localidad, ocupación)
#
def rendimiento_demografico_carrera(session: Session, carrera_id: int) -> schemas.PerformanceDemographic:
    # Busca la carrera por su ID
    carrera = session.get(models.Carreras, carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Consulta estudiantes con sus notas en la carrera
    stmt = (
        select(models.Estudiantes, models.Notas)
        .join(models.Notas, models.Estudiantes.estudiante_id == models.Notas.estudiante_id)
        .join(models.Materia_Carreras, models.Notas.materia_carrera_id == models.Materia_Carreras.id)
        .where(models.Materia_Carreras.carrera_id == carrera_id)
    )
    data = session.exec(stmt).all()

    if not data:
        raise HTTPException(status_code=400, detail="No hay datos suficientes para análisis demográfico")

    # Preparar datos por estudiante
    student_data = {}
    for estudiante, nota in data:
        sid = estudiante.estudiante_id
        if sid not in student_data:
            student_data[sid] = {
                'edad': estudiante.edad,
                'genero': estudiante.genero,
                'localidad': estudiante.localidad,
                'ocupacion': estudiante.ocupacion,
                'notas': []
            }
        student_data[sid]['notas'].append(nota.nota_prom)

    # Calcular promedio y categorizar
    for sid, d in student_data.items():
        if d['notas']:
            avg = sum(d['notas']) / len(d['notas'])
            if avg >= 7.0:
                d['categoria'] = 'promocionado'
            elif avg >= 4.0:
                d['categoria'] = 'regular'
            else:
                d['categoria'] = 'libre'
        else:
            d['categoria'] = 'sin_notas'

    # Inicializar estructura demográfica
    demograficos: Dict[str, Dict[str, schemas.DemographicBreakdown]] = {
        'genero': {},
        'edad': {},
        'localidad': {},
        'ocupacion': {}
    }

    # Agrupar por demográficos
    for d in student_data.values():
        cat = d['categoria']
        if cat == 'sin_notas':
            continue  # Opcional: excluir estudiantes sin notas

        # Género
        gen = d['genero'] or 'no_especificado'
        if gen not in demograficos['genero']:
            demograficos['genero'][gen] = schemas.DemographicBreakdown(promocionado=0, regular=0, libre=0, total=0, promocionado_pct=0.0, regular_pct=0.0, libre_pct=0.0)
        setattr(demograficos['genero'][gen], cat, getattr(demograficos['genero'][gen], cat) + 1)
        demograficos['genero'][gen].total += 1

        # Edad (rangos)
        edad = d['edad']
        if edad is not None:
            if 18 <= edad <= 25:
                rango = '18-25'
            elif 26 <= edad <= 35:
                rango = '26-35'
            elif 36 <= edad <= 45:
                rango = '36-45'
            else:
                rango = '46+'
        else:
            rango = 'no_especificado'
        if rango not in demograficos['edad']:
            demograficos['edad'][rango] = schemas.DemographicBreakdown(promocionado=0, regular=0, libre=0, total=0, promocionado_pct=0.0, regular_pct=0.0, libre_pct=0.0)
        setattr(demograficos['edad'][rango], cat, getattr(demograficos['edad'][rango], cat) + 1)
        demograficos['edad'][rango].total += 1

        # Localidad
        loc = d['localidad'] or 'no_especificado'
        if loc not in demograficos['localidad']:
            demograficos['localidad'][loc] = schemas.DemographicBreakdown(promocionado=0, regular=0, libre=0, total=0, promocionado_pct=0.0, regular_pct=0.0, libre_pct=0.0)
        setattr(demograficos['localidad'][loc], cat, getattr(demograficos['localidad'][loc], cat) + 1)
        demograficos['localidad'][loc].total += 1

        # Ocupación
        ocu = d['ocupacion'] or 'no_especificado'
        if ocu not in demograficos['ocupacion']:
            demograficos['ocupacion'][ocu] = schemas.DemographicBreakdown(promocionado=0, regular=0, libre=0, total=0, promocionado_pct=0.0, regular_pct=0.0, libre_pct=0.0)
        setattr(demograficos['ocupacion'][ocu], cat, getattr(demograficos['ocupacion'][ocu], cat) + 1)
        demograficos['ocupacion'][ocu].total += 1

    # Calcular porcentajes
    for categoria in demograficos.values():
        for subcat_data in categoria.values():
            total = subcat_data.total
            if total > 0:
                subcat_data.promocionado_pct = round((subcat_data.promocionado / total) * 100, 2)
                subcat_data.regular_pct = round((subcat_data.regular / total) * 100, 2)
                subcat_data.libre_pct = round((subcat_data.libre / total) * 100, 2)

    # Retornar resultado
    return schemas.PerformanceDemographic(
        carrera_id=carrera_id,
        carrera_nombre=carrera.nombre,
        demograficos=demograficos
    )
