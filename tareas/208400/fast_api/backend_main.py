# backend_main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

# Load CSV data at startup
data = pd.read_csv("data.csv")

@app.get("/columns/")
def get_columns():
    """Fetch numeric column names from the CSV."""
    columns = data.select_dtypes(include=['float', 'int']).columns.tolist()
    return columns

@app.get("/calculate-stats/{column_name}")
def calculate_stats(column_name: str):
    """Calculate statistics for a specific column."""
    if column_name not in data.columns:
        raise HTTPException(status_code=404, detail="Column not found")

    column_data = data[column_name].dropna()  # Drop any NaN values

    # Calculate statistics
    stats = {
        "mean": column_data.mean(),
        "median": column_data.median(),
        "mode": column_data.mode().tolist(),
        "variance": column_data.var(),
        "std_dev": column_data.std()
    }
    return JSONResponse(content=stats)
