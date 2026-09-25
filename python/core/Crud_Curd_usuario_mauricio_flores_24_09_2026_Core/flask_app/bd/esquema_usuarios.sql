CREATE DATABASE IF NOT EXISTS esquema_usuarios;

USE esquema_usuarios;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nombre, apellido, email)
SELECT "Ricky", "Martin", "ricky@codingdojo.com"
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = "ricky@codingdojo.com");

INSERT INTO usuarios (nombre, apellido, email)
SELECT "Enrique", "Iglesias", "enrique@codingdojo.com"
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = "enrique@codingdojo.com");

INSERT INTO usuarios (nombre, apellido, email)
SELECT "Celia", "Cruz", "celia@codingdojo.com"
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = "celia@codingdojo.com");

INSERT INTO usuarios (nombre, apellido, email)
SELECT "Ricardo", "Montaner", "ricardo@codingdojo.com"
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = "ricardo@codingdojo.com");
