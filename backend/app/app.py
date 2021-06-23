import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

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

@app.get("/")
async def root():
    return {"backend": "Hello world!"}