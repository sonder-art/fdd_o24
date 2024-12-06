from fastapi import FastAPI, UploadFile, File
import pandas as pd
from io import StringIO

app = FastAPI()

@app.post("/analyze/")
async def analyze_data(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))
    summary = df.describe().to_dict()  # Basic summary statistics
    return {"summary": summary}
