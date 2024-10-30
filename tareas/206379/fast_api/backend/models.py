# models.py
from sqlalchemy import Column, Float, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./wines.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class WineDB(Base):
    __tablename__ = "wines"
    
    id = Column(Integer, primary_key=True, index=True)
    fixed_acidity = Column(Float)
    volatile_acidity = Column(Float)
    citric_acid = Column(Float)
    residual_sugar = Column(Float)
    chlorides = Column(Float)
    free_sulfur_dioxide = Column(Float)
    total_sulfur_dioxide = Column(Float)
    density = Column(Float)
    pH = Column(Float)
    sulphates = Column(Float)
    alcohol = Column(Float)
    quality = Column(Integer)

# Pydantic Model
class Wine(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float
    quality: int
    
    class Config:
        orm_mode = True
