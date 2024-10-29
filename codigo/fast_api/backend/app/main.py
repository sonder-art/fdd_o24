from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    text: str

class OutputData(BaseModel):
    message: str

@app.post("/api/hello", response_model=OutputData)
def read_root(data: InputData):
    print(data.text)
    return OutputData(message=f"Received: {data.text}")
