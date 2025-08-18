from app import db, models
from sqlmodel import Session, select

def insert_initial_registers():
    try:
        with Session(db.engine) as session:
            # Insertar carreras
            carreras_data = [
                'Tecnicatura Superior en Ciencia de Datos e I.A',
                'Profesorado de Educación Secundaria en Matemática',
                'Profesorado de Educación Secundaria en Informática'
            ]
            for carrera_nombre in carreras_data:
                # Verificar si la carrera ya existe
                existing_carrera = session.exec(
                    select(models.Carreras).where(models.Carreras.nombre == carrera_nombre)
                ).first()
                if not existing_carrera:
                    nueva_carrera = models.Carreras(nombre=carrera_nombre)
                    session.add(nueva_carrera)
            
            # Commit carreras antes de continuar
            session.commit()

            # Insertar materias
            materias_data = [
                'Alfabetización Académica',
                'Algebra',
                'Algebra 1',
                'Algebra 2',
                'Algoritmos y Programación',
                'Análisis Matemático',
                'Análisis Matemático 1',
                'Análisis Matemático 2',
                'Análisis Matemático 3',
                'Analítica Web',
                'Base de Datos',
                'Cálculo para Informática',
                'Ciberseguridad',
                'Ciencia de Datos',
                'Ciencia y TIC',
                'Conectividad y Redes Informáticas',
                'Didáctica de la Informática',
                'Didáctica de la Matemática',
                'Didáctica General',
                'Diseño de Aplicaciones Informáticas',
                'EDI 1',
                'EDI 2',
                'Educación Sexual Integral',
                'Estadística y Probabilidad',
                'Etica Profesional Docente',
                'Etica y Deontología Profesional',
                'Filosofía',
                'Fisica Matemática',
                'Fundamentos de la Informática',
                'Geometría 1',
                'Geometría 2 y su Didáctica',
                'Gestión de Proyectos',
                'Herramientas Informáticas y Mantenimiento de Equipo',
                'Historia de la Políticas Educativas en la Argentina',
                'Historia y Epistemología de la Matemática',
                'Inglés Técnico',
                'Integración de las TIC en la Enseñanza',
                'Internet y Entornos Virtuales',
                'Introducción a la I.A',
                'Introducción al Análisis Matemático',
                'Lógica',
                'Machine Learning',
                'Matemática Aplicada',
                'Minería de Datos',
                'Pedagogía',
                'Práctica 1',
                'Práctica 2',
                'Práctica 3',
                'Prácticas Profesionalizantes 1',
                'Prácticas Profesionalizantes 2',
                'Prácticas Profesionalizantes 3',
                'Procesamiento del Lenguaje Natural',
                'Programación 1',
                'Programación 2',
                'Programación y Base de Datos',
                'Programación, Diseño y Desarrollo Web',
                'Psicología Educacional',
                'Reconocimiento Visual',
                'Redes',
                'Residencia Pedagógica',
                'Robótica Educativa',
                'Seguridad y Legislación Informática',
                'Sistemas Digitales de la Información',
                'Sociología de la Educación',
                'Software Libre y Proyectos Informáticos',
                'Sujeto de la Educación',
                'Unidad Curricular de Definición Institucional'
            ]
            for materia_nombre in materias_data:
                # Verificar si la materia ya existe
                existing_materia = session.exec(
                    select(models.Materias).where(models.Materias.nombre == materia_nombre)
                ).first()
                if not existing_materia:
                    nueva_materia = models.Materias(nombre=materia_nombre)
                    session.add(nueva_materia)
            
            # Commit materias antes de continuar
            session.commit()

            # Insertar materia_carreras
            materia_carreras_data = [
                '2, 1, 1',
                '6, 1, 1',
                '53, 1, 1',
                '15, 1, 1',
                '11, 1, 1',
                '59, 1, 1',
                '49, 1, 1',
                '21, 1, 1',
                '36, 1, 2',
                '14, 1, 2',
                '24, 1, 2',
                '54, 1, 2',
                '41, 1, 2',
                '39, 1, 2',
                '42, 1, 2',
                '50, 1, 2',
                '22, 1, 2',
                '32, 1, 3',
                '44, 1, 3',
                '58, 1, 3',
                '13, 1, 3',
                '26, 1, 3',
                '10, 1, 3',
                '52, 1, 3',
                '51, 1, 3'
            ]

            for materia_carreras_string in materia_carreras_data:
                # Dividir la cadena en materia_id, carrera_id y anio
                materia_id, carrera_id, anio = map(int, materia_carreras_string.split(', '))

                # Verificar si la materia_carreras ya existe
                existing_materia_carreras = session.exec(
                    select(models.Materia_Carreras).where(models.Materia_Carreras.materia_id == materia_id, models.Materia_Carreras.carrera_id == carrera_id)
                ).first()
                if not existing_materia_carreras:
                    nueva_materia_carreras = models.Materia_Carreras(materia_id=materia_id, carrera_id=carrera_id, anio=anio)
                    session.add(nueva_materia_carreras)
            
            # Commit materia_carreras antes de continuar
            session.commit()

            # Insertar correlativas
            correlativas_data = [
                '10, 4',
                '10, 5',
                '10, 6',
                '11, 1',
                '11, 2',
                '12, 3',
                '12, 5',
                '13, 1',
                '13, 3',
                '13, 5',
                '14, 3',
                '14, 4',
                '14, 5',
                '15, 4',
                '15, 5',
                '15, 6',
                '16, 1',
                '16, 2',
                '16, 3',
                '16, 4',
                '16, 5',
                '16, 6',
                '16, 7',
                '16, 8',
                '18, 15',
                '19, 10',
                '20, 11',
                '20, 13',
                '20, 14',
                '21, 9',
                '21, 14',
                '21, 15',
                '22, 14',
                '22, 15',
                '23, 10',
                '23, 12',
                '23, 13',
                '24, 11',
                '24, 13',
                '24, 14',
                '24, 15',
                '25, 9',
                '25, 10',
                '25, 11',
                '25, 12',
                '25, 13',
                '25, 14',
                '25, 15',
                '25, 16',
                '25, 17'
            ]

            for correlativa_string in correlativas_data:
                # Dividir la cadena en materia_carrera_id y correlativa_id
                materia_carrera_id, correlativa_id = map(int, correlativa_string.split(', '))

                # Verificar si la correlativa ya existe
                existing_correlativa = session.exec(
                    select(models.Correlativas).where(models.Correlativas.materia_carrera_id == materia_carrera_id, models.Correlativas.correlativa_id == correlativa_id)
                ).first()
                if not existing_correlativa:
                    nueva_correlativa = models.Correlativas(materia_carrera_id=materia_carrera_id, correlativa_id=correlativa_id)
                    session.add(nueva_correlativa)

            # # Commit correlativas antes de continuar
            session.commit()

    except Exception as e:
        print(f"❎ Error al insertar registros: {e}")
        session.rollback()
    finally:
        print("🆗 Comprobación de registros finalizada.")
