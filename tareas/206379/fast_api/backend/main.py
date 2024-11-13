from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np

from database import engine, get_db
from models import Base, Wine, WineDB, ColumnRequest

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/wines/", response_model=Wine)
def create_wine(wine: Wine, db: Session = Depends(get_db)):
    db_wine = WineDB(**wine.dict())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return db_wine

@app.get("/wines/", response_model=List[Wine])
def read_wines(db: Session = Depends(get_db)):
    wines = db.query(WineDB).all()
    return wines

@app.get("/wines/columns")
def get_wine_stats(db: Session = Depends(get_db)):
    wines = db.query(WineDB).all()
    
    # Convertir los objetos SQLAlchemy a diccionarios excluyendo los atributos internos
    wine_dicts = []
    for wine in wines:
        wine_dict = {
            'fixed_acidity': wine.fixed_acidity,
            'volatile_acidity': wine.volatile_acidity,
            'citric_acid': wine.citric_acid,
            'residual_sugar': wine.residual_sugar,
            'chlorides': wine.chlorides,
            'free_sulfur_dioxide': wine.free_sulfur_dioxide,
            'total_sulfur_dioxide': wine.total_sulfur_dioxide,
            'density': wine.density,
            'pH': wine.pH,
            'sulphates': wine.sulphates,
            'alcohol': wine.alcohol,
            'quality': wine.quality
        }
        wine_dicts.append(wine_dict)
    
    # Crear DataFrame con los diccionarios
    df = pd.DataFrame(wine_dicts)
    
    if df.empty:
        return {"error": "No data available"}
    
    print(list(df.columns))
    print(df.dtypes)

    return {"columns": list(df.columns)}

@app.post("/wines/columns")
def validate_column(request: ColumnRequest, db: Session = Depends(get_db)):
    column_name = request.column_name
    # Obtener los datos de los vinos
    wines = db.query(WineDB).all()
    wine_dicts = []
    for wine in wines:
        wine_dict = {
            'fixed_acidity': wine.fixed_acidity,
            'volatile_acidity': wine.volatile_acidity,
            'citric_acid': wine.citric_acid,
            'residual_sugar': wine.residual_sugar,
            'chlorides': wine.chlorides,
            'free_sulfur_dioxide': wine.free_sulfur_dioxide,
            'total_sulfur_dioxide': wine.total_sulfur_dioxide,
            'density': wine.density,
            'pH': wine.pH,
            'sulphates': wine.sulphates,
            'alcohol': wine.alcohol,
            'quality': wine.quality
        }
        wine_dicts.append(wine_dict)

    df = pd.DataFrame(wine_dicts)
    
    # Validar que la columna exista
    if column_name not in df.columns:
        return {"error": f"La columna '{column_name}' no existe en los datos."}
    
    # Verificar el tipo de dato de la columna
    column_dtype = df[column_name].dtype
    
    # Determinar las operaciones disponibles
    available_ops = []
    if column_dtype in [pd.Int64Dtype(), pd.Float64Dtype(), np.dtype('int64'), np.dtype('float64')]:
        available_ops = ["mean", "max", "min", "std", "var"]
    elif column_dtype == pd.StringDtype():
        available_ops = ["unique", "value_counts"]
    else:
        available_ops = ["unique"]
    
    return {
        "column_name": column_name,
        "column_type": str(column_dtype),
        "available_operations": available_ops
    }

@app.delete("/wines/{wine_id}")
def delete_wine(wine_id: int, db: Session = Depends(get_db)):
    """Elimina un vino específico por su ID"""
    wine = db.query(WineDB).filter(WineDB.id == wine_id).first()
    if wine is None:
        raise HTTPException(status_code=404, detail="Vino no encontrado")
    
    db.delete(wine)
    db.commit()
    return {"message": f"Vino {wine_id} eliminado exitosamente"}

@app.delete("/wines/delete/all")
def delete_all_wines(db: Session = Depends(get_db)):
    """Elimina todos los vinos de la base de datos"""
    count = db.query(WineDB).delete()
    db.commit()
    return {"message": f"{count} vinos eliminados exitosamente"}

@app.get("/wines/count")
def get_wines_count(db: Session = Depends(get_db)):
    """Obtiene el conteo total de vinos en la base de datos"""
    count = db.query(WineDB).count()
    return {"total": count}

@app.post("/wines/predict_quality")
def predict_quality(wine: Wine, db: Session = Depends(get_db)):
    wines = db.query(WineDB).all()
    df = pd.DataFrame([vars(wine) for wine in wines])
    
    if len(df) < 10:
        raise HTTPException(status_code=400, detail="Not enough training data")
    
    features = [
        'fixed_acidity', 'volatile_acidity', 'citric_acid',
        'residual_sugar', 'chlorides', 'free_sulfur_dioxide',
        'total_sulfur_dioxide', 'density', 'pH', 'sulphates',
        'alcohol'
    ]
    
    X = df[features]
    y = df['quality']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    input_data = pd.DataFrame([wine.dict()])[features]
    prediction = model.predict(input_data)[0]
    
    return {"predicted_quality": round(prediction, 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)