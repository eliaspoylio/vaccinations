from datetime import datetime
from pydantic import BaseModel

class Order(BaseModel):
    id: str
    ordernumber: int
    responsibleperson: str
    healthcaredistrict: str
    vaccine : str
    injections: int
    arrived: datetime

    class Config:
        orm_mode = True

class Vaccination(BaseModel):
    id: str
    sourceBottle: str
    gender: str
    vaccinationDate: datetime

    class Config:
        orm_mode = True