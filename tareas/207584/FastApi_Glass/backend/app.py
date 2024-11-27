from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load the data from the file
data_file_path = "/data/glass.data"

class AnalysisResult(BaseModel):
    mean_values: dict

@app.get("/analyze", response_model=AnalysisResult)
async def analyze():
    # Load the data
    df = pd.read_csv(data_file_path, sep=",", names=["ID", "RI", "NA2O", "MGO", "AL2O3", "SIO2", "K2O", "CAO", "BAO", "FE2O3", "TYPE", "CAMG"])
    
    # Perform basic analysis: calculate the mean of each chemical component
    mean_values = df.drop(columns=["ID", "TYPE"]).mean().to_dict()
    
    return AnalysisResult(mean_values=mean_values)
