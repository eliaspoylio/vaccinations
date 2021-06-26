import os
from sqlalchemy import create_engine

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_URL = os.environ["POSTGRES_URL"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

DB_URL = "postgresql://{user}:{pw}@{url}/{db}".format(user=POSTGRES_USER,pw=POSTGRES_PASSWORD,url=POSTGRES_URL,db=POSTGRES_DB)

engine = create_engine(DB_URL)

conn = engine.connect()
results = conn.execute('SELECT COUNT(id) FROM orders')
print(results.fetchall())
conn.close()

conn = engine.connect()
results = conn.execute("""
SELECT orders.id, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
WHERE arrived < '2021-04-12T11:10:06.473587Z' 
GROUP BY orders.id, orders.injections;
""")
print(results.fetchall())
conn.close()