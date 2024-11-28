from sqlalchemy.orm import Session
from . import models, schemas

# Function to get all transactions
def get_transactions(db: Session):
    return db.query(models.Transaction).all()

# Function to get a specific transaction by ID
def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

# Function to create a new transaction
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Function to delete a transaction by ID
def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
