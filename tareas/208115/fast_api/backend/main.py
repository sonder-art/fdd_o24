from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
from io import StringIO

app = FastAPI()

# Store the uploaded DataFrame in memory
data = None

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global data
    try:
        content = await file.read()
        data = pd.read_csv(StringIO(content.decode("utf-8")))
        return {"message": "File uploaded successfully", "columns": data.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to upload file: {e}")

@app.get("/columns/")
async def get_columns():
    if data is None:
        raise HTTPException(status_code=404, detail="No data available")
    return {"columns": data.columns.tolist()}

class ColumnRequest(BaseModel):
    column: str

@app.post("/statistics/")
async def get_statistics(request: ColumnRequest):
    if data is None:
        raise HTTPException(status_code=404, detail="No data available")
    
    column = request.column
    if column not in data.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    
    if pd.api.types.is_numeric_dtype(data[column]):
        stats = {
            "max": data[column].max(),
            "min": data[column].min(),
            "median": data[column].median(),
            "quantiles": data[column].quantile([0.25, 0.5, 0.75]).to_dict()
        }
        return stats
    else:
        return {"message": "Not a numeric column"}
