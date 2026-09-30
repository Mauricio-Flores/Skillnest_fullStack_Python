CREATE DATABASE IF NOT EXISTS esquema_seguidores
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE esquema_seguidores;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS seguidores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    seguidor_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_seguidores_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    CONSTRAINT fk_seguidores_seguidor
        FOREIGN KEY (seguidor_id) REFERENCES usuarios (id),
    CONSTRAINT uq_usuario_seguidor UNIQUE (usuario_id, seguidor_id)
) ENGINE=InnoDB;

INSERT INTO usuarios (nombre, apellido, email)
VALUES
    ('Soraya', 'Montenegro', 'soraya@example.com'),
    ('Luis F.', 'de la Vega', 'luis@example.com'),
    ('Beatriz', 'Pinzon', 'beatriz@example.com'),
    ('Armando', 'Mendoza', 'armando@example.com'),
    ('Mia', 'Colucci', 'mia@example.com'),
    ('Roberto', 'Pardo', 'roberto@example.com');

INSERT INTO seguidores (usuario_id, seguidor_id)
VALUES
    (1, 2),
    (1, 4),
    (3, 2),
    (5, 2),
    (2, 3);
