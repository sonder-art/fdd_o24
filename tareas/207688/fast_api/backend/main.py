from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/data")
def get_data():
    return {"data": "Sample data from FastAPI"}
