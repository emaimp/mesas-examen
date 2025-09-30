import logging
import pandas as pd
from app import models, schemas
from io import BytesIO
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

#
# Carga Excel con los datos de carreras, materias, materia_carreras y correlativas
#
def cargar_plan_estudio_excel(file_bytes: bytes, session: Session) -> schemas.ApiResponse:
    # Intenta leer el archivo Excel
    try:
        # Lee todas las hojas del Excel
        all_sheets = pd.read_excel(BytesIO(file_bytes), sheet_name=None)

        # Verifica si el archivo está vacío
        if not all_sheets:
            return schemas.ApiResponse(success=False, message="El archivo está vacío o no contiene hojas", errors=[])

        errores_globales = []
        registros_exitosos_totales = 0

        # Procesa la hoja 'Carreras'
        if 'Carreras' in all_sheets:
            df_carreras = all_sheets['Carreras']
            if not df_carreras.empty:
                columnas_requeridas = {'nombre'}
                columnas_faltantes = columnas_requeridas - set(df_carreras.columns)
                if columnas_faltantes:
                    errores_globales.append(f"Hoja 'Carreras': Faltan columnas requeridas: {', '.join(columnas_faltantes)}")
                else:
                    for i, row in df_carreras.iterrows():
                        try:
                            nombre_carrera = str(row['nombre']).strip()
                            if not nombre_carrera:
                                raise ValueError("El nombre de la carrera no puede estar vacío")
                            
                            # Verifica si la carrera ya existe y la añade si no
                            existing_carrera = session.exec(select(models.Carreras).where(models.Carreras.nombre == nombre_carrera)).first()
                            if not existing_carrera:
                                carrera = models.Carreras(nombre=nombre_carrera)
                                session.add(carrera)
                                registros_exitosos_totales += 1
                        except IntegrityError as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Carreras'): Error de integridad (nombre de carrera duplicado) - {str(e)}")
                        except ValueError as e:
                            errores_globales.append(f"Fila {i+2} (Hoja 'Carreras'): Error de datos - {str(e)}")
                        except Exception as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Carreras'): Error inesperado - {str(e)}")
            else:
                errores_globales.append("Hoja 'Carreras': La hoja está vacía")
        else:
            errores_globales.append("Hoja 'Carreras' no encontrada en el archivo Excel")

        # Procesa la hoja 'Materias'
        if 'Materias' in all_sheets:
            df_materias = all_sheets['Materias']
            if not df_materias.empty:
                columnas_requeridas = {'nombre'}
                columnas_faltantes = columnas_requeridas - set(df_materias.columns)
                if columnas_faltantes:
                    errores_globales.append(f"Hoja 'Materias': Faltan columnas requeridas: {', '.join(columnas_faltantes)}")
                else:
                    for i, row in df_materias.iterrows():
                        try:
                            nombre_materia = str(row['nombre']).strip()
                            if not nombre_materia:
                                raise ValueError("El nombre de la materia no puede estar vacío")

                            # Verifica si la materia ya existe y la añade si no
                            existing_materia = session.exec(select(models.Materias).where(models.Materias.nombre == nombre_materia)).first()
                            if not existing_materia:
                                materia = models.Materias(nombre=nombre_materia)
                                session.add(materia)
                                registros_exitosos_totales += 1
                        except IntegrityError as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Materias'): Error de integridad (nombre de materia duplicado) - {str(e)}")
                        except ValueError as e:
                            errores_globales.append(f"Fila {i+2} (Hoja 'Materias'): Error de datos - {str(e)}")
                        except Exception as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Materias'): Error inesperado - {str(e)}")
            else:
                errores_globales.append("Hoja 'Materias': La hoja está vacía")
        else:
            errores_globales.append("Hoja 'Materias' no encontrada en el archivo Excel")

        # Procesa la hoja 'Materia_Carreras'
        if 'Materia_Carreras' in all_sheets:
            df_materia_carreras = all_sheets['Materia_Carreras']
            if not df_materia_carreras.empty:
                columnas_requeridas = {'materia_id', 'carrera_id', 'anio'}
                columnas_faltantes = columnas_requeridas - set(df_materia_carreras.columns)
                if columnas_faltantes:
                    errores_globales.append(f"Hoja 'Materia_Carreras': Faltan columnas requeridas: {', '.join(columnas_faltantes)}")
                else:
                    for i, row in df_materia_carreras.iterrows():
                        try:
                            materia_id = int(row['materia_id'])
                            carrera_id = int(row['carrera_id'])
                            anio = int(row['anio'])

                            # Verifica si la materia y carrera existen
                            materia = session.get(models.Materias, materia_id)
                            carrera = session.get(models.Carreras, carrera_id)

                            if not materia:
                                raise ValueError(f"Materia con ID '{materia_id}' no encontrada para la fila {i+2}")
                            if not carrera:
                                raise ValueError(f"Carrera con ID '{carrera_id}' no encontrada para la fila {i+2}")

                            # Verifica si la relación materia-carrera ya existe y la añade si no
                            existing_materia_carrera = session.exec(
                                select(models.Materia_Carreras).where(
                                    models.Materia_Carreras.materia_id == materia_id,
                                    models.Materia_Carreras.carrera_id == carrera_id
                                )
                            ).first()

                            if not existing_materia_carrera:
                                materia_carrera = models.Materia_Carreras(
                                    materia_id=materia_id,
                                    carrera_id=carrera_id,
                                    anio=anio
                                )
                                session.add(materia_carrera)
                                registros_exitosos_totales += 1
                        except IntegrityError as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Materia_Carreras'): Error de integridad (materia_carrera duplicada) - {str(e)}")
                        except ValueError as e:
                            errores_globales.append(f"Fila {i+2} (Hoja 'Materia_Carreras'): Error de datos - {str(e)}")
                        except Exception as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Materia_Carreras'): Error inesperado - {str(e)}")
            else:
                errores_globales.append("Hoja 'Materia_Carreras': La hoja está vacía")
        else:
            errores_globales.append("Hoja 'Materia_Carreras' no encontrada en el archivo Excel")

        # Procesa la hoja 'Correlativas'
        if 'Correlativas' in all_sheets:
            df_correlativas = all_sheets['Correlativas']
            if not df_correlativas.empty:
                columnas_requeridas = {'materia_carrera_id', 'correlativa_id'}
                columnas_faltantes = columnas_requeridas - set(df_correlativas.columns)
                if columnas_faltantes:
                    errores_globales.append(f"Hoja 'Correlativas': Faltan columnas requeridas: {', '.join(columnas_faltantes)}")
                else:
                    for i, row in df_correlativas.iterrows():
                        try:
                            materia_carrera_id = int(row['materia_carrera_id'])
                            correlativa_id = int(row['correlativa_id'])

                            # Verifica si las relaciones materia-carrera existen
                            materia_principal_mc = session.get(models.Materia_Carreras, materia_carrera_id)
                            correlativa_mc = session.get(models.Materia_Carreras, correlativa_id)

                            if not materia_principal_mc:
                                raise ValueError(f"Materia_Carrera principal con ID '{materia_carrera_id}' no encontrada para la fila {i+2}")
                            if not correlativa_mc:
                                raise ValueError(f"Materia_Carrera correlativa con ID '{correlativa_id}' no encontrada para la fila {i+2}")

                            # Verifica si la correlativa ya existe y la añade si no
                            existing_correlativa = session.exec(
                                select(models.Correlativas).where(
                                    models.Correlativas.materia_carrera_id == materia_carrera_id,
                                    models.Correlativas.correlativa_id == correlativa_id
                                )
                            ).first()

                            if not existing_correlativa:
                                correlativa = models.Correlativas(
                                    materia_carrera_id=materia_carrera_id,
                                    correlativa_id=correlativa_id
                                )
                                session.add(correlativa)
                                registros_exitosos_totales += 1
                        except IntegrityError as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Correlativas'): Error de integridad (correlativa duplicada) - {str(e)}")
                        except ValueError as e:
                            errores_globales.append(f"Fila {i+2} (Hoja 'Correlativas'): Error de datos - {str(e)}")
                        except Exception as e:
                            session.rollback()
                            errores_globales.append(f"Fila {i+2} (Hoja 'Correlativas'): Error inesperado - {str(e)}")
            else:
                errores_globales.append("Hoja 'Correlativas': La hoja está vacía")
        else:
            errores_globales.append("Hoja 'Correlativas' no encontrada en el archivo Excel")

        # Intenta guardar los cambios en la base de datos
        try:
            session.commit()
            return schemas.ApiResponse(
                success=registros_exitosos_totales > 0 and not errores_globales,
                message=f"{registros_exitosos_totales} registros cargados correctamente (carreras, materias y correlativas)."
                           if registros_exitosos_totales > 0 else "No se cargaron registros",
                errors=errores_globales
            )
        # Manejo de errores al guardar en la base de datos
        except IntegrityError as e:
            session.rollback()
            return schemas.ApiResponse(success=False, message="No se pudo cargar el archivo, valores duplicados", errors=[])
        except Exception as e:
            session.rollback()
            return schemas.ApiResponse(success=False, message="Error al guardar los datos en la base de datos", errors=[str(e)])

    # Manejo de errores generales al procesar el archivo
    except Exception as e:
        return schemas.ApiResponse(success=False, message="Error procesando el archivo", errors=[str(e)])
