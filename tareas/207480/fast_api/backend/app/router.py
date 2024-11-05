#backend/router.py
from fastapi import APIRouter, HTTPException
from .models import Item
import pandas as pd
import os

router = APIRouter()

# Sample in-memory storage
items = []


csv_path = os.path.join(os.path.dirname(__file__), 'winequality-red.csv')
wine_data = pd.read_csv(csv_path, sep=';')


@router.get("/items/")
async def get_items():
  return items

@router.post("/items/")
async def create_item(item: Item):
  items.append(item)
  return item

@router.get("/columns/")
async def get_columns():
  """Get the list of columns from the wine DataFrame."""
  return [col.strip() for col in wine_data.columns.tolist()]

@router.get("/statistics/{column_name}/")
async def get_statistics(column_name: str):
  """Get statistics for a specified column."""
  if column_name not in wine_data.columns:
    raise HTTPException(status_code=404, detail="Column not found")

  mean = wine_data[column_name].mean()
  variance = wine_data[column_name].var()
  std_dev = wine_data[column_name].std()

  return {"mean": mean, "variance": variance, "std_dev": std_dev}