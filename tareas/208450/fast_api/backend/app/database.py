# backend/app/database.py
from pymongo import MongoClient

def get_database():
    client = MongoClient("mongodb://mongodb:27017/")
    return client["online_retail_db"]

