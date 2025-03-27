import pandas as pd

# Datos de los ayuntamientos con coordenadas
ayuntamientos_coords = [
    ("Málaga", 36.7213, -4.4212),
    ("Granada", 37.1773, -3.5986),
    ("Santiago de Compostela", 42.8805, -8.5457)
]

# Crear DataFrame de ayuntamientos
df_ayuntamientos = pd.DataFrame(ayuntamientos_coords, columns=["nombre", "latitud", "longitud"])

# Datos de las oposiciones
oposiciones_data = [
    ("Málaga", "Profesor", "2025-04-01"),
    ("Granada", "Arquitecto", "2025-04-02"),
    ("Santiago de Compostela", "Ingeniero", "2025-04-03"),
    ("Málaga", "Abogado", "2025-04-04"),
    ("Granada", "Médico", "2025-04-05")
]

# Crear DataFrame de oposiciones
df_oposiciones = pd.DataFrame(oposiciones_data, columns=["ayuntamiento", "oposicion", "fecha"])

# Crear un archivo Excel con dos hojas: "ayuntamientos" y "oposiciones"
excel_file = 'ayuntamientos_oposiciones.xlsx'
with pd.ExcelWriter(excel_file) as writer:
    df_ayuntamientos.to_excel(writer, sheet_name="ayuntamientos", index=False)
    df_oposiciones.to_excel(writer, sheet_name="oposiciones", index=False)

print(f"Archivo Excel '{excel_file}' creado exitosamente.")



