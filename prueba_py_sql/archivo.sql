CREATE DATABASE library;
USE library;

CREATE TABLE usuarios (
id_usuario INT PRIMARY KEY AUTO_INCREMENT,
nombre VARCHAR(50) NOT NULL,
correo VARCHAR(120) UNIQUE,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
deleted BOOLEAN DEFAULT 0
);

CREATE TABLE libros (
id_libro INT PRIMARY KEY AUTO_INCREMENT,
titulo VARCHAR(80) NOT NULL,
autor VARCHAR(100) NOT NULL,
stock INT DEFAULT 1,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
deleted BOOLEAN DEFAULT 0
);

CREATE TABLE prestamos (
    id_prestamo INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    fecha_prestamo DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    estado INT DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro)
);

INSERT INTO usuarios (nombre, correo,created_at)  
VALUES ('Akon', 'akon@gmail.com', NOW());

INSERT INTO libros (titulo, autor, created_at)  
VALUES ('Cien años de soledad', 'Gabriel García Márquez', NOW());

INSERT INTO libros (titulo, autor, created_at)  
VALUES ('El principito', 'Antoine de Saint-Exupéry', NOW());

INSERT INTO libros(titulo, autor, created_at)
VALUES ('Don Quijote de la Mancha', 'Miguel de Cervantes');

SELECT * FROM usuarios;
SELECT * FROM libros;