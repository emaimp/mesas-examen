import pandas as pd
from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#
# Predice el rendimiento futuro de una carrera usando ML (Random Forest)
#
def prediccion_rendimiento_carrera(session: Session, carrera_id: int) -> schemas.PerformanceCareer:
    # Busca la carrera por su ID
    carrera = session.get(models.Carreras, carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Obtener el año de ingreso más reciente para predicción
    max_anio_stmt = select(models.Estudiantes.anio_ingreso).where(models.Estudiantes.carrera_id == carrera_id).order_by(models.Estudiantes.anio_ingreso.desc()).limit(1)
    max_anio_result = session.exec(max_anio_stmt).first()
    if not max_anio_result:
        raise HTTPException(status_code=404, detail="No hay estudiantes en la carrera")
    latest_anio = max_anio_result

    # Datos históricos para entrenamiento (año anterior al más reciente)
    historical_stmt = (
        select(models.Estudiantes, models.Notas)
        .join(models.Notas, models.Estudiantes.estudiante_id == models.Notas.estudiante_id)
        .join(models.Materia_Carreras, models.Notas.materia_carrera_id == models.Materia_Carreras.id)
        .where(models.Materia_Carreras.carrera_id == carrera_id)
        .where(models.Estudiantes.anio_ingreso < latest_anio)
    )
    historical_data = session.exec(historical_stmt).all()

    if not historical_data:
        raise HTTPException(status_code=400, detail="No hay datos históricos suficientes para entrenar el modelo")

    # Preparar datos para ML
    data = []
    for estudiante, nota in historical_data:
        # Calcular target basado en promedio, pero simplificar: usar nota_prom como proxy
        if nota.nota_prom >= 7.0:
            target = 0  # promocionado
        elif nota.nota_prom >= 4.0:
            target = 1  # regular
        else:
            target = 2  # libre
        data.append({
            'estudiante_id': estudiante.estudiante_id,
            'anio_ingreso': estudiante.anio_ingreso,
            'nota_prom': nota.nota_prom,
            'target': target
        })

    df = pd.DataFrame(data)

    # Agrupar por estudiante para features agregadas
    df_grouped = df.groupby('estudiante_id').agg({
        'anio_ingreso': 'first',
        'nota_prom': 'mean',
        'target': 'first'  # Target basado en promedio
    }).reset_index()

    if len(df_grouped) < 10:
        raise HTTPException(status_code=400, detail="Insuficientes datos históricos para modelo confiable")

    # Features and target
    X = df_grouped[['anio_ingreso', 'nota_prom']]
    y = df_grouped['target']

    # Split de datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar modelo
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)

    # Evaluación rápida (opcional, no devolver al usuario)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo: {accuracy:.2f}")  # Debug (remueve en producción)

    # Datos para predicción (estudiantes del último año)
    current_stmt = (
        select(models.Estudiantes, models.Notas)
        .join(models.Notas, models.Estudiantes.estudiante_id == models.Notas.estudiante_id, isouter=True)  # Left join en caso de notas faltantes
        .join(models.Materia_Carreras, models.Notas.materia_carrera_id == models.Materia_Carreras.id, isouter=True)
        .where(models.Estudiantes.carrera_id == carrera_id)
        .where(models.Estudiantes.anio_ingreso == latest_anio)
    )
    current_data = session.exec(current_stmt).all()

    if not current_data:
        raise HTTPException(status_code=404, detail="No hay estudiantes para predecir")

    # Preparar features para predicción
    pred_data = []
    for estudiante, nota in current_data:
        nota_prom_val = nota.nota_prom if nota else 4.0  # Si no hay nota, asumir promedio bajo
        pred_data.append({
            'estudiante_id': estudiante.estudiante_id,
            'anio_ingreso': estudiante.anio_ingreso,
            'nota_prom': nota_prom_val
        })

    pred_df = pd.DataFrame(pred_data).drop_duplicates(subset='estudiante_id')
    if pred_df.empty:
        raise HTTPException(status_code=400, detail="No hay estudiantes válidos para predicción")

    X_pred = pred_df[['anio_ingreso', 'nota_prom']]
    predictions = model.predict(X_pred)

    # Contar predicciones
    promocionados_count = 0
    regulares_count = 0
    libres_count = 0
    for pred in predictions:
        if pred == 0:  # promocionado
            promocionados_count += 1
        elif pred == 1:  # regular
            regulares_count += 1
        elif pred == 2:  # libre
            libres_count += 1

    total_students_pred = len(predictions)
    promocionados_percentage = round((promocionados_count / total_students_pred * 100), 2) if total_students_pred > 0 else 0.0
    regulares_percentage = round((regulares_count / total_students_pred * 100), 2) if total_students_pred > 0 else 0.0
    libres_percentage = round((libres_count / total_students_pred * 100), 2) if total_students_pred > 0 else 0.0

    # Retorna objeto similar a rendimiento_carrera pero con predicciones
    return schemas.PerformanceCareer(
        carrera_id=carrera_id,
        carrera_nombre=carrera.nombre,
        promocionados_count=promocionados_count,
        promocionados_percentage=promocionados_percentage,
        regulares_count=regulares_count,
        regulares_percentage=regulares_percentage,
        libres_count=libres_count,
        libres_percentage=libres_percentage,
        total_notas_evaluadas=total_students_pred  # Usar como total estudiantes predichos
    )
