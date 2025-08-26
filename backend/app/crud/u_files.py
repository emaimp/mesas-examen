import pandas as pd
from app import crud, models, schemas
from io import BytesIO
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

#
# Carga Excel con los datos de los usuarios y sus asignaciones
#
def cargar_usuarios_excel(file_bytes: bytes, session: Session) -> schemas.ApiResponse:
    # Intenta leer el archivo Excel
    try:
        # Lee todas las hojas del Excel
        all_sheets = pd.read_excel(BytesIO(file_bytes), sheet_name=None)
        
        # Verifica si el archivo está vacío
        if not all_sheets:
            return schemas.ApiResponse(success=False, message="El archivo está vacío o no contiene hojas", errors=[])

        errores_globales = []
        registros_exitosos_totales = 0

        # Itera sobre cada hoja del Excel
        for sheet_name, df in all_sheets.items():
            # Define las columnas base requeridas para los usuarios
            columnas_base_requeridas = {'username', 'password', 'role', 'nombre', 'dni', 'email'}
            columnas_faltantes = columnas_base_requeridas - set(df.columns)
            
            # Verifica si faltan columnas requeridas
            if columnas_faltantes:
                errores_globales.append(f"Hoja '{sheet_name}': Faltan columnas requeridas: {', '.join(columnas_faltantes)}")
                continue
            
            # Verifica si la hoja está vacía
            if df.empty:
                errores_globales.append(f"Hoja '{sheet_name}': El archivo está vacío")
                continue
            
            errores_hoja = []
            registros_exitosos_hoja = 0

            # Itera sobre cada fila de la hoja
            for i, row in df.iterrows():
                try:
                    # Prepara los datos del usuario
                    user_data = {
                        "username": str(row['username']).strip(),
                        "password": str(row['password']).strip(),
                        "role": str(row['role']).strip(),
                        "nombre": str(row['nombre']).strip(),
                        "dni": str(row['dni']).strip(),
                        "email": str(row['email']).strip() if pd.notna(row['email']) else None,
                        "legajo": str(row['legajo']).strip() if 'legajo' in df.columns and pd.notna(row['legajo']) else None,
                        "libreta": str(row['libreta']).strip() if 'libreta' in df.columns and pd.notna(row['libreta']) else None,
                    }

                    # Crea el usuario en la base de datos
                    user_in = schemas.UserCreate(**user_data)
                    user = crud.cr_usuarios.create_user(session=session, user_in=user_in)
                    
                    # Si el rol es estudiante, crea el registro de estudiante
                    if user.role == "student":
                        # Valida campos específicos para estudiantes
                        if 'carrera_id' not in df.columns or pd.isna(row['carrera_id']):
                            raise ValueError("El campo 'carrera_id' es requerido para estudiantes")
                        if 'anio_ingreso' not in df.columns or pd.isna(row['anio_ingreso']):
                            raise ValueError("El campo 'anio_ingreso' es requerido para estudiantes")
                        
                        estudiante_data = schemas.StudentCreate(
                            estudiante_id=user.id,
                            carrera_id=int(row['carrera_id']),
                            anio_ingreso=int(row['anio_ingreso'])
                        )
                        crud.cr_estudiantes.create_estudiante(session=session, estudiante_in=estudiante_data)
                    
                    # Si el rol es profesor, crea el registro de profesor
                    elif user.role == "teacher":
                        # Valida campos específicos para profesores
                        if 'materia_carrera_id' not in df.columns or pd.isna(row['materia_carrera_id']):
                            raise ValueError("El campo 'materia_carrera_id' es requerido para profesores")
                        if 'anio_asignado' not in df.columns or pd.isna(row['anio_asignado']):
                            raise ValueError("El campo 'anio_asignado' es requerido para profesores")

                        profesor_data = schemas.TeacherCreate(
                            profesor_id=user.id,
                            materia_carrera_id=int(row['materia_carrera_id']),
                            anio_asignado=int(row['anio_asignado'])
                        )
                        crud.cr_profesores.create_profesor(session=session, profesor_in=profesor_data)
                    
                    registros_exitosos_hoja += 1
                # Manejo de errores específicos
                except IntegrityError as e:
                    session.rollback()
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error de integridad (ej usuario/DNI/email/libreta/legajo duplicado o asignación duplicada) - {str(e)}")
                except ValueError as e:
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error de datos - {str(e)}")
                except Exception as e:
                    session.rollback()
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error inesperado - {str(e)}")
            
            registros_exitosos_totales += registros_exitosos_hoja
            errores_globales.extend(errores_hoja)
        
        # Intenta guardar los cambios en la base de datos
        try:
            session.commit()
            return schemas.ApiResponse(
                success=registros_exitosos_totales > 0,
                message=f"{registros_exitosos_totales} usuarios cargados correctamente"
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
                message=f"{registros_exitosos} notas cargadas/actualizadas correctamente"
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

#
# Carga Excel con los datos de carreras, materias, materia_carreras y correlativas
#
def cargar_carreras_materias_correlativas_excel(file_bytes: bytes, session: Session) -> schemas.ApiResponse:
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
                message=f"{registros_exitosos_totales} registros de carreras, materias y correlativas cargados correctamente"
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
