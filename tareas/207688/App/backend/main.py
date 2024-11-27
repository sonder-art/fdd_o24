# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect("wine_data.db")
    conn.row_factory = sqlite3.Row
    return conn

# Modelo Pydantic para los datos del vino
class WineItem(BaseModel):
    Class: int
    Alcohol: float
    Malic_acid: float
    Ash: float
    Alcalinity_of_ash: float
    Magnesium: int
    Total_phenols: float
    Flavanoids: float
    Nonflavanoid_phenols: float
    Proanthocyanins: float
    Color_intensity: float
    Hue: float
    OD280_OD315: float
    Proline: int

@app.get("/wines")
def get_wines():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wine")
    wines = cursor.fetchall()
    conn.close()
    return {"data": [dict(wine) for wine in wines]}

@app.post("/wines")
def add_wine(wine: WineItem):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO wine (Class, Alcohol, Malic_acid, Ash, Alcalinity_of_ash, "
        "Magnesium, Total_phenols, Flavanoids, Nonflavanoid_phenols, Proanthocyanins, "
        "Color_intensity, Hue, OD280_OD315, Proline) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (wine.Class, wine.Alcohol, wine.Malic_acid, wine.Ash, wine.Alcalinity_of_ash, 
         wine.Magnesium, wine.Total_phenols, wine.Flavanoids, wine.Nonflavanoid_phenols, 
         wine.Proanthocyanins, wine.Color_intensity, wine.Hue, wine.OD280_OD315, wine.Proline)
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.delete("/wines")
def delete_wine(wine_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wine WHERE rowid = ?", (wine_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}
