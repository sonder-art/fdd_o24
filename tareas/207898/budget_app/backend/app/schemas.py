from pydantic import BaseModel

class TransactionBase(BaseModel):
    date: str
    description: str
    amount: float
    category: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True


