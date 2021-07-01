FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN python -m pip install --upgrade pip

RUN python -m pip install sqlalchemy psycopg2 pytest requests

COPY ./app /app