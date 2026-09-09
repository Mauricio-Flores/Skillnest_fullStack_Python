CREATE DATABASE IF NOT EXISTS primera_flask
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE primera_flask;
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    edad INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- La identidad del seed es nombre/tipo/color, nunca un id fijo.
INSERT INTO mascotas (nombre, tipo, color)
SELECT 'Firulais', 'Perro', 'Café'
WHERE NOT EXISTS (
    SELECT 1 FROM mascotas WHERE nombre = 'Firulais' AND tipo = 'Perro'
        AND color = 'Café'
);

INSERT INTO mascotas (nombre, tipo, color)
SELECT 'Michi', 'Gato', 'Negro'
WHERE NOT EXISTS (
    SELECT 1 FROM mascotas WHERE nombre = 'Michi' AND tipo = 'Gato' AND color = 'Negro'
);

INSERT INTO mascotas (nombre, tipo, color)
SELECT 'Luna', 'Perro', 'Blanco'
WHERE NOT EXISTS (
    SELECT 1 FROM mascotas WHERE nombre = 'Luna' AND tipo = 'Perro' AND color = 'Blanco'
);

INSERT INTO mascotas (nombre, tipo, color)
SELECT 'Nala', 'Gato', 'Naranjo'
WHERE NOT EXISTS (
    SELECT 1 FROM mascotas WHERE nombre = 'Nala' AND tipo = 'Gato' AND color = 'Naranjo'
);

INSERT INTO mascotas (nombre, tipo, color)
SELECT 'Coco', 'Conejo', 'Blanco'
WHERE NOT EXISTS (
    SELECT 1 FROM mascotas WHERE nombre = 'Coco' AND tipo = 'Conejo' AND color = 'Blanco'
);

INSERT INTO usuarios (nombre, email, edad)
SELECT 'Ana Torres', 'ana.torres@example.com', 24
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = 'ana.torres@example.com');

INSERT INTO usuarios (nombre, email, edad)
SELECT 'Luis Soto', 'luis.soto@example.com', 31
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = 'luis.soto@example.com');

INSERT INTO usuarios (nombre, email, edad)
SELECT 'Eva Rojas', 'eva.rojas@example.com', 27
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = 'eva.rojas@example.com');
