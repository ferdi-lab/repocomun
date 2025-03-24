CREATE DATABASE IF NOT EXISTS wikipediaDB;
USE wikipediaDB;

CREATE TABLE paises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE contenido_extraido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pais_id INT NOT NULL,
    superficie VARCHAR(255),
    poblacion VARCHAR(255),
    pib_ppa VARCHAR(255),
    FOREIGN KEY (pais_id) REFERENCES paises(id) ON DELETE CASCADE
);

-- Ejemplo de inserción de datos extraídos
INSERT INTO paises (nombre) VALUES ('Alemania');
INSERT INTO contenido_extraido (pais_id, superficie, poblacion, pib_ppa) 
VALUES (1, '357.022 km²', '83.24 millones', '4.5 billones USD');
