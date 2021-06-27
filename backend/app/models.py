from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(String)
    ordernumber = Column(Integer, primary_key=True)
    responsibleperson = Column(String)
    healthcaredistrict = Column(String)
    vaccine = Column(String)
    injections = Column(Integer)
    arrived = Column(TIMESTAMP)

class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(String, primary_key=True)
    sourcebottle = Column(String)
    gender = Column(String)
    vaccinationdate = Column(TIMESTAMP)