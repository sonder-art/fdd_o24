from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import pandas as pd

app = FastAPI()

# Variable global para almacenar el DataFrame después de cargarlo
df = None

# Modelo para definir la solicitud de operación
class OperationRequest(BaseModel):
    column: str
    operation: str
    second_column: Optional[str] = None  # Para operaciones que requieren dos columnas (ej. gráficos)

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...), delimiter: str = Query(',')):
    global df
    try:
        # Leer el archivo y convertirlo a un DataFrame con el delimitador especificado
        df = pd.read_csv(file.file, delimiter=delimiter)
        column_names = df.columns.tolist()
        column_types = df.dtypes.astype(str).tolist()

        # Regresar las columnas y sus tipos al frontend
        return {"columns": column_names, "types": column_types}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@app.post("/operation/")
async def perform_operation(request: OperationRequest):
    global df
    try:
        # Verificar que el DataFrame esté cargado
        if df is None:
            raise HTTPException(status_code=400, detail="No file uploaded. Please upload a file first.")

        # Realizar la operación solicitada
        result = None
        if request.operation == "mean":
            result = df[request.column].mean()
        elif request.operation == "max":
            result = df[request.column].max()
        elif request.operation == "var":
            result = df[request.column].var()
        elif request.operation == "graph" and request.second_column:
            # Regresa los datos para graficar si se eligen dos columnas
            result = df[[request.column, request.second_column]].to_dict(orient="records")
        else:
            raise ValueError("Operación no soportada o columnas inválidas.")

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error performing operation: {str(e)}")

