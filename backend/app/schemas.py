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
        #allow_population_by_field_name = True

class Vaccination(BaseModel):
    id: str
    sourcebottle: str
    gender: str
    vaccinationdate: datetime

    class Config:
        orm_mode = True