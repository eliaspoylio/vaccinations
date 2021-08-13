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
    'http://localhost:3000', # app in frontend container
    'http://localhost:8081', # cypress server
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

@app.get("/orders/count")
def show_orders_arrived_count(db: Session = Depends(get_db)):
    statement = select(func.count(models.Order.ordernumber))
    result = db.execute(statement).all()
    return result

@app.get("/vaccinations/count")
def show_orders_arrived_count(db: Session = Depends(get_db)):
    statement = select(func.count(models.Vaccination.id))
    result = db.execute(statement).all()
    return result


@app.get("/orders/total/{day}")
def show_orders_arrived_total(day, db: Session = Depends(get_db)):
    statement = select(func.count(models.Order.id)
                       ).where(models.Order.arrived <= day)
    result = db.execute(statement).all()
    return result

@app.get("/vaccinations/total/{day}")
def show_vaccinations_arrived_total(day, db: Session = Depends(get_db)):
    statement = select(func.sum(models.Order.injections)
                       ).where(models.Order.arrived <= day)
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

@app.get("/orders/expired/{day}")
def show_orders_expired_day(day, db: Session = Depends(get_db)):
    statement = text("""
    WITH ordersused AS (
    SELECT orders.id, arrived + interval '30 days' AS "expires", COUNT(vaccinations.sourceBottle) AS "used",
    injections - COUNT(vaccinations.sourceBottle) AS "unused"
    FROM orders
    FULL OUTER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
    GROUP BY orders.id, orders.arrived, orders.injections
    )
    SELECT COUNT(id)
    FROM ordersused
    WHERE expires < :day;
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

@app.get("/vaccinations/left/{day}")
def show_vaccinations_left_day(day, db: Session = Depends(get_db)):
    statement = text("""
    WITH injectionsused AS (
    SELECT orders.id, arrived + interval '30 days' AS "expires", orders.injections - COUNT(vaccinations.sourceBottle) AS "vunused"
    FROM orders
    INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
    WHERE vaccinations.vaccinationDate <= :day
    GROUP BY orders.id, orders.arrived, orders.injections
    )
    SELECT SUM(vunused)
    FROM injectionsused
    WHERE expires > :day;
    """)
    result = db.execute(statement, {'day': day}).all()
    return result

@app.get("/vaccinations/expiring_tendays/{day}")
def test_show_vaccinations_expiring_tendays(day, db: Session = Depends(get_db)):
    statement = text("""
    WITH injectionsused AS (
    SELECT orders.id, arrived + interval '30 days' AS "expires", orders.injections - COUNT(vaccinations.sourceBottle) AS "vunused"
    FROM orders
    INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
    WHERE vaccinations.vaccinationDate <= :day
    GROUP BY orders.id, orders.arrived, orders.injections
    )
    SELECT SUM(vunused)
    FROM injectionsused
    WHERE expires < DATE(:day) + interval '10' day AND expires > :day;
    """)
    result = db.execute(statement, {'day': day}).all()
    return result

@app.get("/orders/day/{day}")
def show_orders_arrived_day(day, db: Session = Depends(get_db)):
    statement = select(func.count(models.Order.id)).where(
        cast(models.Order.arrived, DATE) == day)
    result = db.execute(statement).all()
    return result

@app.get("/manufacturer/total/{day}")
def show_manufacturer_total_day(day, db: Session = Depends(get_db)):
    statement = text("""
    SELECT vaccine, COUNT(id) AS orders, SUM(injections) AS injections FROM orders WHERE arrived < :day GROUP BY vaccine ORDER BY vaccine;
    """)
    result = db.execute(statement, {'day': day}).all()
    return result

@app.get("/district/total/{day}")
def show_district_total_day(day, db: Session = Depends(get_db)):
    statement = text("""
    SELECT healthcaredistrict, COUNT(id) AS orders, SUM(injections) AS injections FROM orders WHERE arrived <= :day GROUP BY healthcaredistrict ORDER BY healthcaredistrict;
    """)
    result = db.execute(statement, {'day': day}).all()
    return result

@app.get("/timeseries")
def show_timeseries(db: Session = Depends(get_db)):
    statement = text("""
    WITH ordates AS (
      SELECT
      date_trunc('day', arrived) AS "day",
      count(orders.id) AS "orders",
      sum(injections) AS "injections"
      FROM orders
      GROUP BY day
      )
    SELECT 
    date(ordates.day) AS day,
    ordates.orders,
    ordates.injections,
    count(vaccinations.id) AS "vaccinations" 
    FROM ordates
    FULL OUTER JOIN vaccinations ON ordates.day=date_trunc('day', vaccinations.vaccinationDate)
    GROUP BY day, ordates.orders, ordates.injections
    ORDER BY day;
    """)
    result = db.execute(statement).all()
    return result

@app.get("/gender/total/{day}")
def show_gender_total_day(day, db: Session = Depends(get_db)):
    statement = text("""
    SELECT gender, COUNT(id)
    FROM vaccinations 
    WHERE DATE(vaccinationDate) = DATE(:day) 
    GROUP BY gender 
    ORDER BY gender;
    """)
    result = db.execute(statement, {'day': day}).all()
    return result