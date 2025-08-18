-- Tabla: Usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    role VARCHAR(10) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    dni VARCHAR(10) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE,
    legajo VARCHAR(10) UNIQUE,
    libreta VARCHAR(10) UNIQUE,
    INDEX username_index (username),
    INDEX nombre_index (nombre)
);

-- Tabla: Profesores
CREATE TABLE profesores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profesor_id INT NOT NULL,
    materia_carrera_id INT NOT NULL,
    anio_asignado INT NOT NULL,
    UNIQUE (profesor_id, materia_carrera_id, anio_asignado),
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id),
    FOREIGN KEY (materia_carrera_id) REFERENCES materia_carreras(id)
);

-- Tabla: Estudiantes
CREATE TABLE estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    estudiante_id INT NOT NULL,
    carrera_id INT NOT NULL,
    anio_ingreso INT NOT NULL,
    UNIQUE (estudiante_id, carrera_id, anio_ingreso),
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id),
    FOREIGN KEY (carrera_id) REFERENCES carreras(id)
);

-- Tabla: Carreras
CREATE TABLE carreras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: Materias
CREATE TABLE materias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: Materia_Carreras
CREATE TABLE materia_carreras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    materia_id INT NOT NULL,
    carrera_id INT NOT NULL,
    anio INT,
    UNIQUE (materia_id, carrera_id),
    FOREIGN KEY (materia_id) REFERENCES materias(id),
    FOREIGN KEY (carrera_id) REFERENCES carreras(id)
);

-- Tabla: Notas
CREATE TABLE notas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    estudiante_id INT NOT NULL,
    materia_carrera_id INT NOT NULL,
    eval_1 INT NOT NULL,
    rec_1 INT NOT NULL,
    eval_2 INT NOT NULL,
    rec_2 INT NOT NULL,
    eval_3 INT NOT NULL,
    rec_3 INT NOT NULL,
    nota_prom FLOAT NOT NULL,
    UNIQUE (estudiante_id, materia_carrera_id),
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id),
    FOREIGN KEY (materia_carrera_id) REFERENCES materia_carreras(id),
    CHECK (eval_1 BETWEEN 0 AND 10),
    CHECK (rec_1 BETWEEN 0 AND 10),
    CHECK (eval_2 BETWEEN 0 AND 10),
    CHECK (rec_2 BETWEEN 0 AND 10),
    CHECK (eval_3 BETWEEN 0 AND 10),
    CHECK (rec_3 BETWEEN 0 AND 10)
);

-- Tabla: Practicos
CREATE TABLE practicos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    estudiante_id INT NOT NULL,
    materia_carrera_id INT NOT NULL,
    tp_1 INT NOT NULL,
    tp_2 INT NOT NULL,
    tp_3 INT NOT NULL,
    tp_4 INT NOT NULL,
    tp_5 INT NOT NULL,
    tp_6 INT NOT NULL,
    tp_7 INT NOT NULL,
    tp_8 INT NOT NULL,
    tp_9 INT NOT NULL,
    tp_10 INT NOT NULL,
    UNIQUE (estudiante_id, materia_carrera_id),
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id),
    FOREIGN KEY (materia_carrera_id) REFERENCES materia_carreras(id),
    CHECK (tp_1 BETWEEN 0 AND 10),
    CHECK (tp_2 BETWEEN 0 AND 10),
    CHECK (tp_3 BETWEEN 0 AND 10),
    CHECK (tp_4 BETWEEN 0 AND 10),
    CHECK (tp_5 BETWEEN 0 AND 10),
    CHECK (tp_6 BETWEEN 0 AND 10),
    CHECK (tp_7 BETWEEN 0 AND 10),
    CHECK (tp_8 BETWEEN 0 AND 10),
    CHECK (tp_9 BETWEEN 0 AND 10),
    CHECK (tp_10 BETWEEN 0 AND 10)
);

-- Tabla: Correlativas
CREATE TABLE correlativas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    materia_carrera_id INT NOT NULL,
    correlativa_id INT NOT NULL,
    UNIQUE (materia_carrera_id, correlativa_id),
    FOREIGN KEY (materia_carrera_id) REFERENCES materia_carreras(id),
    FOREIGN KEY (correlativa_id) REFERENCES materia_carreras(id)
);

-- Tabla: Mesas_Examen
CREATE TABLE mesas_examen (
    id INT PRIMARY KEY AUTO_INCREMENT,
    materia_carrera_id INT NOT NULL,
    profesor_id INT NOT NULL,
    fecha DATETIME NOT NULL,
    UNIQUE (materia_carrera_id, fecha),
    FOREIGN KEY (materia_carrera_id) REFERENCES materia_carreras(id),
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id)
);

-- Tabla: Inscripciones_Examen
CREATE TABLE inscripciones_examen (
    id INT PRIMARY KEY AUTO_INCREMENT,
    estudiante_id INT NOT NULL,
    mesa_examen_id INT NOT NULL,
    fecha_inscripcion DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    estado VARCHAR(20) DEFAULT 'active' NOT NULL,
    UNIQUE (estudiante_id, mesa_examen_id),
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id),
    FOREIGN KEY (mesa_examen_id) REFERENCES mesas_examen(id)
);
