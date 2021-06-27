import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy import text, func, select

from . import models, schemas
from typing import List


app = FastAPI()

origins = [
    'http://localhost',
    'localhost'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"backend": "Hello world!"}

@app.get("/orders/", response_model=List[schemas.Order])
def show_records(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders

@app.get("/vaccinations/", response_model=List[schemas.Vaccination])
def show_records(db: Session = Depends(get_db)):
    vaccinations = db.query(models.Vaccination).all()
    return vaccinations

@app.get("/injections/{day}")
def show_records(day, db: Session = Depends(get_db)):
    statement = select(func.sum(models.Order.injections)).where(models.Order.arrived<day)
    result = db.execute(statement).all()
    return result