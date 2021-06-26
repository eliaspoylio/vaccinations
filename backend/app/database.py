import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_URL = os.environ["POSTGRES_URL"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

DB_URL = "postgresql://{user}:{pw}@{url}/{db}".format(user=POSTGRES_USER,pw=POSTGRES_PASSWORD,url=POSTGRES_URL,db=POSTGRES_DB)

engine = create_engine(
    DB_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()