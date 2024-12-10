from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    value: int

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_value": item.value}
