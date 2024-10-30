# backend/app/main.py
from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np 
from .database import get_database
from .crud import save_data, get_columns, calculate_statistic, most_frequent_value, prepare_graph_data
from .models import CalculationResult
from bson import ObjectId

app = FastAPI()
db = get_database()

@app.on_event("startup")
async def startup_event():
    try:
        data = pd.read_excel("/app/online_retail.xlsx")
        save_data(db, data)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Failed to load data: {e}")
        
# Endpoint to get first few rows (head) of the dataset
@app.get("/head/")
async def get_head():
    collection = db["data"]
    data = pd.DataFrame(list(collection.find().limit(10)))
    
    if data.empty:
        raise HTTPException(status_code=404, detail="No data available.")

    # Convert ObjectId fields to strings
    for column in data.columns:
        data[column] = data[column].apply(lambda x: str(x) if isinstance(x, ObjectId) else x)
    
    return {"head": data.to_dict(orient="records")}

# Endpoint to get column names and types
@app.get("/columns/")
async def list_columns():
    collection = db["data"]
    sample = collection.find_one()
    if not sample:
        raise HTTPException(status_code=404, detail="No data available in the database.")
    
    # Define column types
    column_types = {}
    for col, value in sample.items():
        if col == "InvoiceNo":
            column_types[col] = "string"
        elif col == "_id":
            column_types[col] = "object"
        elif col == "InvoiceDate":
            column_types[col] = "datetime"
        elif isinstance(value, (int, float)):
            column_types[col] = "numeric"
        elif isinstance(value, str):
            column_types[col] = "string"
        else:
            column_types[col] = "unknown"
    return column_types

@app.get("/calculate/", response_model=CalculationResult)
async def calculate(column: str, operation: str):
    collection = db["data"]
    data = pd.DataFrame(list(collection.find()))

    if column not in data.columns:
        raise HTTPException(status_code=404, detail=f"Column '{column}' not found in the dataset.")

    if data[column].dtype not in [float, int, 'float64', 'int64']:
        raise HTTPException(status_code=400, detail=f"Column '{column}' is not numeric and cannot be used for statistical calculations.")

    result = None
    if operation == "mean":
        result = data[column].mean()
    elif operation == "variance":
        result = data[column].var()
    elif operation == "max":
        result = data[column].max()
    elif operation == "min":
        result = data[column].min()
    else:
        raise HTTPException(status_code=400, detail=f"Operation '{operation}' is not supported.")

    # Round the result to two decimal places if it's numeric
    if isinstance(result, (np.generic, np.ndarray)):
        result = result.item()
    
    if isinstance(result, (float, int)):
        result = round(result, 2)

    return {"column": column, "operation": operation, "result": result}

@app.get("/most_frequent/")
async def most_frequent(column: str):
    result = most_frequent_value(db, column)
    if result is None:
        raise HTTPException(status_code=400, detail="Column not found or not string type")
    return {"column": column, "most_frequent": result}

@app.get("/graph/")
async def graph(column: str, group_by: str = None):
    data = prepare_graph_data(db, column, group_by)
    if data is None:
        raise HTTPException(status_code=400, detail="Invalid column or group_by option")
    return {"data": data}






