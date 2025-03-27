import pandas as pd
import sqlite3

def excel_to_sqlite(excel_file, db_name):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Crear tabla de ayuntamientos con coordenadas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ayuntamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            latitud REAL,
            longitud REAL
        )
    ''')
    
    # Insertar coordenadas manualmente
    ayuntamientos_coords = [
        ("Málaga", 36.7213, -4.4212),
        ("Granada", 37.1773, -3.5986),
        ("Santiago de Compostela", 42.8805, -8.5457)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO ayuntamientos (nombre, latitud, longitud) 
        VALUES (?, ?, ?)''', ayuntamientos_coords)
    
    # Leer el archivo Excel
    xls = pd.ExcelFile(excel_file)
    
    # Crear tabla de oposiciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS oposiciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayuntamiento TEXT,
            oposicion TEXT,
            fecha TEXT,
            FOREIGN KEY (ayuntamiento) REFERENCES ayuntamientos(nombre)
        )
    ''')
    
    # Insertar datos en la tabla de oposiciones
    df = xls.parse(xls.sheet_names[0])
    df.to_sql("oposiciones", conn, if_exists='replace', index=False)
    
    # Mostrar las tablas creadas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tablas creadas:")
    for table in tables:
        print(table[0])
        
        # Mostrar las primeras filas de cada tabla
        df = pd.read_sql_query(f"SELECT * FROM {table[0]} LIMIT 5", conn)
        print(df)
    
    # Guardar y cerrar conexión
    conn.commit()
    conn.close()

# Uso del script
excel_to_sqlite('ayuntamientos_oposiciones.xlsx', 'ayuntamientos.db')
