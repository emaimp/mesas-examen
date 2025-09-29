import logging
import pandas as pd
from app import crud, models, schemas
from io import BytesIO
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

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
        registros_ignorados_totales = 0

        # Define las hojas a procesar con roles esperados
        sheets_to_process = {
            'Estudiantes': 'student',
            'Profesores': 'teacher'
        }

        # Itera sobre las hojas requeridas
        for sheet_name, expected_role in sheets_to_process.items():
            if sheet_name not in all_sheets:
                errores_globales.append(f"Hoja requerida '{sheet_name}' no encontrada en el Excel")
                continue

            df = all_sheets[sheet_name]

            # Define las columnas base requeridas para los usuarios
            columnas_base_requeridas = {'username', 'password', 'role', 'nombre', 'dni', 'email'}
            columnas_faltantes = columnas_base_requeridas - set(df.columns)

            # Verifica si faltan columnas requeridas
            if columnas_faltantes:
                errores_globales.append(f"Hoja '{sheet_name}': Faltan columnas requeridas: {', '.join(columnas_faltantes)}")
                continue

            # Verifica si la hoja está vacía
            if df.empty:
                errores_globales.append(f"Hoja '{sheet_name}': La hoja está vacía")
                continue
            
            errores_hoja = []
            users_to_create = []
            rows_to_process_after_user_creation = []

            # Primera pasada: Recopilar usuarios nuevos y hashear contraseñas
            for i, row in df.iterrows():
                try:
                    role = str(row['role']).strip()

                    # Validar que el rol coincida con el esperado para la hoja
                    if role != expected_role:
                        errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): El rol '{role}' no coincide con el esperado para esta hoja ('{expected_role}')")
                        continue

                    user_data = {
                        "username": str(row['username']).strip(),
                        "password": str(row['password']).strip(),
                        "role": role,
                        "nombre": str(row['nombre']).strip(),
                        "dni": str(row['dni']).strip(),
                        "email": str(row['email']).strip() if pd.notna(row['email']) else None,
                        "legajo": str(row['legajo']).strip() if 'legajo' in df.columns and pd.notna(row['legajo']) else None,
                        "libreta": str(row['libreta']).strip() if 'libreta' in df.columns and pd.notna(row['libreta']) else None,
                    }
                    user_in = schemas.UserCreate(**user_data)

                    existing_user = crud.cr_usuarios.get_user_by_unique_fields(session=session, user_in=user_in)

                    if existing_user:
                        registros_ignorados_totales += 1
                    else:
                        users_to_create.append(user_in)
                        rows_to_process_after_user_creation.append((i, row)) # Guardar la fila original para procesar asignaciones
                except ValueError as e:
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error de datos - {str(e)}")
                except Exception as e:
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error inesperado en pre-procesamiento - {str(e)}")
            
            # Insertar todos los usuarios nuevos en un solo lote
            created_users = []
            if users_to_create:
                try:
                    created_users = crud.cr_usuarios.create_multiple_users(session=session, users_in=users_to_create)
                    registros_exitosos_totales += len(created_users)
                except IntegrityError as e:
                    session.rollback()
                    errores_globales.append(f"Hoja '{sheet_name}': Error de integridad al insertar usuarios en lote - {str(e)}")
                    # Si hay un error de integridad en el lote, no podemos confiar en los IDs, así que salimos de esta hoja
                    errores_globales.extend(errores_hoja)
                    continue
                except Exception as e:
                    session.rollback()
                    errores_globales.append(f"Hoja '{sheet_name}': Error inesperado al insertar usuarios en lote - {str(e)}")
                    errores_globales.extend(errores_hoja)
                    continue

            # Mapear los usuarios creados a sus datos originales para procesar asignaciones
            user_map = {user.username: user for user in created_users}

            # Segunda pasada: Crear asignaciones para estudiantes y profesores
            for i, row in rows_to_process_after_user_creation:
                try:
                    username = str(row['username']).strip()
                    user = user_map.get(username) # Obtener el usuario recién creado
                    
                    if not user: # Esto no debería pasar si el flujo es correcto, pero es una salvaguarda
                        errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error interno: Usuario no encontrado después de la creación en lote - {username}")
                        continue

                    # Si el rol es estudiante, crea el registro de estudiante
                    if user.role == "student":
                        if 'carrera' not in df.columns or pd.isna(row['carrera']):
                            raise ValueError("El campo 'carrera' es requerido para estudiantes")
                        if 'añio ingreso' not in df.columns or pd.isna(row['añio ingreso']):
                            raise ValueError("El campo 'añio ingreso' es requerido para estudiantes")

                        # Resolver el nombre de la carrera a su ID numérico
                        carrera_nombre = str(row['carrera']).strip()
                        carrera = session.exec(select(models.Carreras).where(models.Carreras.nombre == carrera_nombre)).first()
                        if not carrera:
                            raise ValueError(f"Carrera '{carrera_nombre}' no encontrada en la base de datos")
                        carrera_id_resuelto = carrera.id

                        estudiante_data = schemas.StudentCreate(
                            estudiante_id=user.id,
                            carrera_id=carrera_id_resuelto,
                            anio_ingreso=int(row['añio ingreso'])
                        )
                        crud.cr_estudiantes.create_estudiante(session=session, estudiante_in=estudiante_data)
                    
                    # Si el rol es profesor, crea el registro de profesor
                    elif user.role == "teacher":
                        if 'materia' not in df.columns or pd.isna(row['materia']):
                            raise ValueError("El campo 'materia' es requerido para profesores")
                        if 'carrera' not in df.columns or pd.isna(row['carrera']):
                            raise ValueError("El campo 'carrera' es requerido para profesores")
                        if 'añio asignado' not in df.columns or pd.isna(row['añio asignado']):
                            raise ValueError("El campo 'añio asignado' es requerido para profesores")

                        # Resolver los nombres de materia y carrera a materia_carrera_id numérico
                        materia_nombre = str(row['materia']).strip()
                        carrera_nombre = str(row['carrera']).strip()
                        # Query JOIN para encontrar Materia_Carreras: Materias.nombre + Carreras.nombre
                        statement = select(models.Materia_Carreras).join(models.Materias).join(models.Carreras).where(
                            models.Materias.nombre == materia_nombre,
                            models.Carreras.nombre == carrera_nombre
                        )
                        matching_materia_carreras = session.exec(statement).all()
                        if not matching_materia_carreras:
                            raise ValueError(f"Materia_Carrera no encontrada para materia '{materia_nombre}' en carrera '{carrera_nombre}' en la base de datos")
                        if len(matching_materia_carreras) > 1:
                            raise ValueError(f"Ambiguedad: Encontradas múltiples Materia_Carrera para materia '{materia_nombre}' en carrera '{carrera_nombre}'\nAsegúrese de que la combinación sea única")
                        materia_carrera_id_resuelto = matching_materia_carreras[0].id

                        profesor_data = schemas.TeacherCreate(
                            profesor_id=user.id,
                            materia_carrera_id=materia_carrera_id_resuelto,
                            anio_asignado=int(row['añio asignado'])
                        )
                        crud.cr_profesores.create_profesor(session=session, profesor_in=profesor_data)
                    
                except IntegrityError as e:
                    session.rollback()
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error de integridad (ej asignación duplicada) - {str(e)}")
                except ValueError as e:
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error de datos en asignación - {str(e)}")
                except Exception as e:
                    session.rollback()
                    errores_hoja.append(f"Fila {i+2} (Hoja '{sheet_name}'): Error inesperado en asignación - {str(e)}")
            
            errores_globales.extend(errores_hoja)
        
        # Registrar todos los errores detallados en el log del servidor
        for error_msg in errores_globales:
            logger.error(error_msg)

        # Construir el mensaje para el frontend
        final_message = ""
        success_status = False

        ignored_info = f" {registros_ignorados_totales} usuarios ignorados (usuarios existentes)." if registros_ignorados_totales > 0 else ""

        if registros_exitosos_totales > 0 and len(errores_globales) == 0:
            final_message = f"{registros_exitosos_totales} usuarios cargados correctamente.{ignored_info}"
            success_status = True
        elif registros_exitosos_totales > 0 and len(errores_globales) > 0:
            final_message = f"{registros_exitosos_totales} usuarios cargados, pero ocurrieron {len(errores_globales)} errores.{ignored_info}"
            success_status = True # Consideramos éxito parcial para el frontend
        elif registros_exitosos_totales == 0 and len(errores_globales) > 0:
            final_message = f"No se pudo cargar ningún usuario debido a {len(errores_globales)} errores.{ignored_info}"
            success_status = False
        else: # No se cargaron registros y no hay errores específicos
            final_message = f"No se cargaron registros de usuarios.{ignored_info}".strip() if ignored_info else "No se cargaron registros de usuarios."
            success_status = False

        # Intenta guardar los cambios en la base de datos
        try:
            session.commit()
            return schemas.ApiResponse(
                success=success_status,
                message=final_message,
                errors=[] # Vaciar la lista de errores para el frontend
            )
        # Manejo de errores al guardar en la base de datos (errores de commit final)
        except IntegrityError as e:
            session.rollback()
            logger.error(f"Error de integridad al guardar los datos finales: {str(e)}")
            return schemas.ApiResponse(success=False, message="Error al guardar los datos finales: valores duplicados.", errors=[])
        except Exception as e:
            session.rollback()
            logger.error(f"Error inesperado al guardar los datos finales: {str(e)}")
            return schemas.ApiResponse(success=False, message="Error inesperado al guardar los datos finales.", errors=[])
    # Manejo de errores generales al procesar el archivo
    except Exception as e:
        logger.error(f"Error general procesando el archivo Excel: {str(e)}")
        return schemas.ApiResponse(success=False, message="Error procesando el archivo Excel.", errors=[])
