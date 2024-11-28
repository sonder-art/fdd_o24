# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI Backend") #Here we are creating an instance of FastAPI and passing the title as FastAPI Backend.
#The title is the title of the API that will be displayed in the documentation.

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
