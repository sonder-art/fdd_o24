# backend/load_data.py
import sqlite3
import pandas as pd

# Descargar el archivo 'wine.data' y cargarlo
df = pd.read_csv("wine.data", header=None)
df.columns = [
    "Class", "Alcohol", "Malic_acid", "Ash", "Alcalinity_of_ash", 
    "Magnesium", "Total_phenols", "Flavanoids", "Nonflavanoid_phenols", 
    "Proanthocyanins", "Color_intensity", "Hue", "OD280_OD315", "Proline"
]

# Conexión a la base de datos SQLite
conn = sqlite3.connect("wine_data.db")
df.to_sql("wine", conn, if_exists="replace", index=False)
conn.close()

print("Datos de vino cargados en la base de datos SQLite.")
