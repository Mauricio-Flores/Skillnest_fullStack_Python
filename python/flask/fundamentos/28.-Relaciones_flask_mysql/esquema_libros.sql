-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_libros;

USE esquema_libros;


-- ==========================================================
-- TABLA AUTORES
-- ==========================================================

CREATE TABLE IF NOT EXISTS autores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA LIBROS
-- ==========================================================

CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(45),
    genero VARCHAR(45),
    editorial VARCHAR(45),
    autor_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_libros_autores
        FOREIGN KEY (autor_id)
        REFERENCES autores(id)
);


-- ==========================================================
-- AUTORES DE PRUEBA
-- ==========================================================

INSERT INTO autores
(nombre)
VALUES
("Gabriel García Márquez"),
("Isabel Allende"),
("Julio Cortázar");


-- ==========================================================
-- LIBROS DE PRUEBA
-- ==========================================================

INSERT INTO libros
(
    titulo,
    genero,
    editorial,
    autor_id
)
VALUES
(
    "Cien años de soledad",
    "Novela",
    "Sudamericana",
    1
),
(
    "El coronel no tiene quien le escriba",
    "Novela",
    "Oveja Negra",
    1
),
(
    "La casa de los espíritus",
    "Novela",
    "Plaza & Janés",
    2
),
(
    "Eva Luna",
    "Novela",
    "Plaza & Janés",
    2
),
(
    "Rayuela",
    "Novela",
    "Sudamericana",
    3
);
