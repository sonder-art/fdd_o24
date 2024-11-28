from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to read all transactions
@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db)
    return transactions

# Endpoint to create a new transaction
@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

# Endpoint to delete a transaction by ID
@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction_by_id(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    crud.delete_transaction(db, transaction_id)
    return {"message": "Transaction deleted successfully"}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Budget App API"}
