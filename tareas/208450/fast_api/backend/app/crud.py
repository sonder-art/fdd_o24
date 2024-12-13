# backend/app/crud.py
import pandas as pd
from pymongo.collection import Collection

def save_data(db, data: pd.DataFrame):
    collection = db["data"]
    collection.delete_many({})  # Clear old data
    collection.insert_many(data.to_dict("records"))

def get_columns(db) -> list:
    collection = db["data"]
    if (sample := collection.find_one()) is not None:
        return list(sample.keys())
    return []

def calculate_statistic(db, column: str, operation: str):
    collection = db["data"]
    data = pd.DataFrame(list(collection.find()))
    if column not in data.columns:
        return None

    operations = {
        "mean": data[column].mean,
        "max": data[column].max,
        "min": data[column].min,
        "var": data[column].var,
    }
    if operation in operations:
        return operations[operation]()
    return None

def most_frequent_value(db, column: str):
    collection = db["data"]
    data = pd.DataFrame(list(collection.find()))
    if column in data.columns and data[column].dtype == "object":
        return data[column].mode()[0]
    return None

def prepare_graph_data(db, column: str, group_by: str = None):
    collection = db["data"]
    data = pd.DataFrame(list(collection.find()))
    if column not in data.columns:
        return None
    
    # Prepare data based on grouping
    if group_by and group_by in data.columns:
        if pd.api.types.is_datetime64_any_dtype(data[group_by]):
            data[group_by] = pd.to_datetime(data[group_by])
        grouped_data = data.groupby(group_by)[column].sum().reset_index()
    else:
        grouped_data = data[[column]]
    
    return grouped_data.to_dict(orient="records")
