import logging
import pandas as pd
from app import models, schemas
from io import BytesIO
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

#
# Carga Excel con las notas de los estudiantes
#
def cargar_notas_excel(file_bytes: bytes, session: Session) -> schemas.ApiResponse:
    # Intenta leer el archivo Excel
    try:
        df = pd.read_excel(BytesIO(file_bytes))
        
        # Columnas requeridas para las notas
        columnas_requeridas = {'estudiante_id', 'materia_carrera_id', 'nota_prom'}
        
        # Verifica si faltan columnas requeridas
        columnas_faltantes = columnas_requeridas - set(df.columns)
        if columnas_faltantes:
            return schemas.ApiResponse(
                success=False,
                message=f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}",
                errors=[]
            )
        
        # Verifica si el archivo está vacío
        if df.empty:
            return schemas.ApiResponse(success=False, message="El archivo está vacío", errors=[])
        
        errores = []
        registros_exitosos = 0

        # Itera sobre cada fila del archivo
        for i, row in df.iterrows():
            try:
                # Extrae y convierte los datos de la fila
                estudiante_id = int(row['estudiante_id'])
                materia_carrera_id = int(row['materia_carrera_id'])
                nota_prom = float(row['nota_prom'])

                # Extrae notas de evaluaciones y recuperatorios
                eval_1 = int(row['eval_1']) if 'eval_1' in df.columns and pd.notna(row['eval_1']) else 0
                rec_1 = int(row['rec_1']) if 'rec_1' in df.columns and pd.notna(row['rec_1']) else 0
                eval_2 = int(row['eval_2']) if 'eval_2' in df.columns and pd.notna(row['eval_2']) else 0
                rec_2 = int(row['rec_2']) if 'rec_2' in df.columns and pd.notna(row['rec_2']) else 0
                eval_3 = int(row['eval_3']) if 'eval_3' in df.columns and pd.notna(row['eval_3']) else 0
                rec_3 = int(row['rec_3']) if 'rec_3' in df.columns and pd.notna(row['rec_3']) else 0

                # Verifica si el estudiante existe y es válido
                estudiante = session.get(models.Usuarios, estudiante_id)
                if not estudiante or estudiante.role != "student":
                    raise ValueError("Estudiante no encontrado o no es un estudiante válido")
                
                # Verifica si la materia existe
                materia_carrera = session.get(models.Materia_Carreras, materia_carrera_id)
                if not materia_carrera:
                    raise ValueError("Materia no encontrada")
                
                # Verifica si el estudiante está asignado a una carrera
                estudiante_record = session.exec(select(models.Estudiantes).where(models.Estudiantes.estudiante_id == estudiante_id)).first()
                if not estudiante_record:
                    raise ValueError("El estudiante no está asignado a una carrera")

                # Verifica si la materia pertenece a la carrera del estudiante
                if materia_carrera.carrera_id != estudiante_record.carrera_id:
                    raise ValueError("La materia no pertenece al plan de carrera del estudiante")
                
                # Busca si ya existe una nota para este estudiante y materia
                existing_nota_statement = select(models.Notas).where(
                    models.Notas.estudiante_id == estudiante_id,
                    models.Notas.materia_carrera_id == materia_carrera_id
                )
                existing_nota = session.exec(existing_nota_statement).first()

                # Si la nota existe, la actualiza, si no, crea una nueva
                if existing_nota:
                    existing_nota.eval_1 = eval_1
                    existing_nota.rec_1 = rec_1
                    existing_nota.eval_2 = eval_2
                    existing_nota.rec_2 = rec_2
                    existing_nota.eval_3 = eval_3
                    existing_nota.rec_3 = rec_3
                    existing_nota.nota_prom = nota_prom
                    session.add(existing_nota)
                else:
                    nota = models.Notas(
                        estudiante_id=estudiante_id,
                        materia_carrera_id=materia_carrera_id,
                        eval_1=eval_1,
                        rec_1=rec_1,
                        eval_2=eval_2,
                        rec_2=rec_2,
                        eval_3=eval_3,
                        rec_3=rec_3,
                        nota_prom=nota_prom
                    )
                    session.add(nota)
                
                registros_exitosos += 1
            # Manejo de errores específicos
            except IntegrityError as e:
                session.rollback()
                errores.append(f"Fila {i+2}: Error de integridad (ej nota duplicada) - {str(e)}")
            except ValueError as e:
                errores.append(f"Fila {i+2}: Error de datos - {str(e)}")
            except Exception as e:
                errores.append(f"Fila {i+2}: Error inesperado - {str(e)}")
        
        # Intenta guardar los cambios en la base de datos
        try:
            session.commit()
            return schemas.ApiResponse(
                success=registros_exitosos > 0,
                message=f"{registros_exitosos} notas cargadas/actualizadas correctamente."
                           if registros_exitosos > 0 else "No se cargaron registros",
                errors=errores
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
