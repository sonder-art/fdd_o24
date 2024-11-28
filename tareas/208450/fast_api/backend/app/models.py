# backend/app/models.py
from pydantic import BaseModel
from typing import Union

class StatisticRequest(BaseModel):
    column: str
    operation: str

class CalculationResult(BaseModel):
    column: str
    operation: str
    result: Union[float, str]  # Float for numerical results, str for any errors


