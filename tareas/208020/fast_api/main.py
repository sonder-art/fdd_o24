# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os

app = FastAPI()

class DataRequest(BaseModel):
    filename: str  # Accepts the filename as input
    column: str

def load_csv_from_file(filename: str):
    # Check if the file exists in the current working directory
    if not os.path.isfile(filename):
        raise HTTPException(status_code=400, detail="File not found.")

    # Attempt to read the CSV file with different encodings
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']
    for encoding in encodings_to_try:
        try:
            return pd.read_csv(filename, encoding=encoding)
        except Exception as e:
            # Print the error for debugging (optional)
            print(f"Failed to read with encoding {encoding}: {e}")
    raise HTTPException(status_code=400, detail="Failed to read CSV file with supported encodings.")

@app.post("/metrics")
async def calculate_metrics(request: DataRequest):
    try:
        data = load_csv_from_file(request.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if request.column not in data.columns:
        return {"error": "Column not found"}

    column_data = data[request.column]
    metrics = {}

    if pd.api.types.is_numeric_dtype(column_data):
        metrics["mean"] = column_data.mean()
        metrics["std_dev"] = column_data.std()
        metrics["min"] = column_data.min()
        metrics["max"] = column_data.max()
    else:
        metrics["mode"] = column_data.mode()[0]
        metrics["frequency"] = column_data.value_counts().to_dict()
    
    return metrics
