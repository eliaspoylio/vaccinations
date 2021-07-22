import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy import text, func, select, cast, DATE

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
def show_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders


@app.get("/vaccinations/", response_model=List[schemas.Vaccination])
def show_vaccinations(db: Session = Depends(get_db)):
    vaccinations = db.query(models.Vaccination).all()
    return vaccinations


@app.get("/injections/total/{day}")
def show_injections_arrived_total(day, db: Session = Depends(get_db)):
    statement = select(func.sum(models.Order.injections)
                       ).where(models.Order.arrived < day)
    result = db.execute(statement).all()
    return result


@app.get("/orders/day/{day}")
def show_orders_arrived_day(day, db: Session = Depends(get_db)):
    statement = select(func.count(models.Order.id)).where(
        cast(models.Order.arrived, DATE) == day)
    result = db.execute(statement).all()
    return result

@app.get("/vaccinations/used/{day}")
def show_vaccinations_used_day(day, db: Session = Depends(get_db)):
    statement = text("""
    WITH injectionsused AS (
    SELECT orders.id, orders.injections, COUNT(vaccinations.sourceBottle) AS "vused"
    FROM orders
    INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
    WHERE vaccinations.vaccinationDate < :day 
    GROUP BY orders.id, orders.injections
    )
    SELECT SUM(vused)
    FROM injectionsused;
    """)
    result = db.execute(statement, {'day': day}).all()
    return result


@app.get("/vaccinations/expired/{day}")
def show_orders_arrived_day(day, db: Session = Depends(get_db)):
    statement = text("""
    WITH ordersused AS (
    SELECT orders.id, arrived + interval '30 days' AS "expires", COUNT(vaccinations.sourceBottle) AS "used",
    injections - COUNT(vaccinations.sourceBottle) AS "unused"
    FROM orders
    FULL OUTER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
    GROUP BY orders.id, orders.arrived, orders.injections
    )
    SELECT SUM(unused)
    FROM ordersused
    WHERE expires < :day;
    """)
    result = db.execute(statement, {'day': day}).all()
    return result
