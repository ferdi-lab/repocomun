import sqlite3

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect('wikipediaDB.db')

# Crear las tablas y realizar la inserción de datos
query = '''
-- Crear la tabla "paises"
CREATE TABLE IF NOT EXISTS paises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);
'''
query = '''

CREATE TABLE contenido_extraido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pais_id INT NOT NULL,
    superficie VARCHAR(255),
    poblacion VARCHAR(255),
    pib_ppa VARCHAR(255),
    FOREIGN KEY (pais_id) REFERENCES paises(id) ON DELETE CASCADE
);

'''

# Ejecutar la consulta
conn.executescript(query)

# Confirmar que se realizó correctamente
conn.commit()

# Cerrar la conexión
conn.close()

print("Datos insertados correctamente.")
