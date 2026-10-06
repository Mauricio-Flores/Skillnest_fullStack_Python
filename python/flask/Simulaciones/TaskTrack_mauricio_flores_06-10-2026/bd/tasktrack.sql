DROP DATABASE IF EXISTS tasktrack;
CREATE DATABASE tasktrack CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tasktrack;

CREATE TABLE usuarios (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_usuarios_email (email)
) ENGINE=InnoDB;

CREATE TABLE categorias (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(80) NOT NULL,
    usuario_id INT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_categoria_usuario (usuario_id, nombre),
    CONSTRAINT fk_categorias_usuarios
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE tareas (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    prioridad ENUM('Alta', 'Media', 'Baja') NOT NULL,
    estado ENUM('Pendiente', 'En progreso', 'Completada') NOT NULL DEFAULT 'Pendiente',
    fecha_limite DATE NOT NULL,
    usuario_id INT UNSIGNED NOT NULL,
    categoria_id INT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_tareas_usuario_fecha (usuario_id, fecha_limite),
    KEY idx_tareas_categoria (categoria_id),
    CONSTRAINT fk_tareas_usuarios
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_tareas_categorias
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE comentarios (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    contenido VARCHAR(500) NOT NULL,
    usuario_id INT UNSIGNED NOT NULL,
    tarea_id INT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_comentarios_tarea (tarea_id, created_at),
    CONSTRAINT fk_comentarios_usuarios
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_comentarios_tareas
        FOREIGN KEY (tarea_id) REFERENCES tareas(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;
