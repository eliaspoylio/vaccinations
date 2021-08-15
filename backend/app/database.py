import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_URL = os.environ.get("POSTGRES_URL", "postgres:5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "vaccinations")

DB_URL = "postgresql://{user}:{pw}@{url}/{db}".format(user=POSTGRES_USER,pw=POSTGRES_PASSWORD,url=POSTGRES_URL,db=POSTGRES_DB)

engine = create_engine(
    DB_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()