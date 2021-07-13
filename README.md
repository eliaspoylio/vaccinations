Create `.env` file:
```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_URL=postgres:5432
POSTGRES_DB=vaccinations
```
`docker-compose --env-file .env up --build`

docker exec -it vaccinations_postgres_1 bash
psql -h localhost -p 5432 -U postgres -W

cat psql.sh | docker exec -it vaccinations_postgres_1 bash

psql postgresql://postgres:1234@localhost:5432/postgres

```sql
postgres=# SELECT COUNT(id) FROM orders WHERE arrived < '2021-04-12T11:10:06.473587Z';
 count
-------
  5000
(1 row)

postgres=# SELECT SUM(injections) FROM orders WHERE arrived < '2021-04-12T11:10:06.473587Z';
  sum
-------
 25015
(1 row)

postgres=# SELECT COUNT(id) FROM vaccinations WHERE vaccinationdate < '2021-04-12T11:10:06.473587Z';
 count
-------
  7000
(1 row)

postgres=# SELECT vaccine, COUNT(id) FROM orders WHERE arrived < '2021-04-12T11:10:06.473587Z' GROUP BY vaccine;
    vaccine    | count
---------------+-------
 SolarBuddhica |  1676
 Zerpfy        |  1663
 Antiqua       |  1661
(3 rows)

postgres=# SELECT vaccine, SUM(injections) FROM orders WHERE arrived < '2021-04-12T11:10:06.473587Z' GROUP BY vaccine;
    vaccine    |  sum
---------------+-------
 SolarBuddhica | 10056
 Zerpfy        |  8315
 Antiqua       |  6644
(3 rows)

SELECT orders.id, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
WHERE arrived < '2021-04-12T11:10:06.473587Z' 
GROUP BY orders.id, orders.injections;

SELECT orders.arrived, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
GROUP BY orders.arrived, orders.injections;

WITH used AS (
SELECT orders.id, orders.arrived, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT SUM(used."vaccinations unused")
FROM used
WHERE DATE(arrived) + interval '30 days' < '2021-04-14';
---------
WITH used AS (
SELECT orders.id, orders.arrived, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
LEFT JOIN vaccinations ON orders.id = vaccinations.sourceBottle
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT id, DATE(arrived), injections, used."vaccinations used", used."vaccinations unused"
FROM used
GROUP BY id, arrived, injections, used."vaccinations used", used."vaccinations unused";
----------------

WITH used AS (
SELECT orders.id, orders.arrived, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
LEFT JOIN vaccinations ON orders.id = vaccinations.sourceBottle
--WHERE arrived < '2021-04-12T11:10:06.473587Z'
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT COUNT(used."vaccinations unused")
FROM used
WHERE arrived + interval '30 days' <= '2021-04-12T11:10:06.473587Z';
------------------

WITH used AS (
SELECT orders.id, orders.arrived, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
LEFT JOIN vaccinations ON orders.id = vaccinations.sourceBottle
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT SUM(used."vaccinations unused")
FROM used
WHERE arrived + interval '30 days' <= '2021-04-12T11:10:06.473587Z';
----------------------
WITH used AS (
SELECT orders.id, orders.arrived, orders.arrived + interval '30 days' AS "expires", orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
LEFT JOIN vaccinations ON orders.id = vaccinations.sourceBottle
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT id, DATE(arrived), expires ,injections, used."vaccinations used", used."vaccinations unused"
FROM used
GROUP BY id, arrived, expires, injections, used."vaccinations used", used."vaccinations unused";
---------------------------
WITH ordersused AS (
SELECT orders.id, arrived, arrived + interval '30 days' AS "expires", injections, COUNT(vaccinations.sourceBottle) AS "used",
injections - COUNT(vaccinations.sourceBottle) AS "unused"
FROM orders
FULL OUTER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT SUM(unused)
--SELECT id, arrived, expires, injections, used, unused
FROM ordersused
WHERE expires < '2021-04-12T11:10:06.473587Z';

-----------

SELECT COUNT(id)
FROM orders
WHERE DATE(arrived) = '2021-03-20';
```

```
WITH used AS (
SELECT orders.id, DATE(arrived), DATE(arrived) + interval '30 days' AS "expires", injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
LEFT JOIN vaccinations ON orders.id = vaccinations.sourceBottle
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT SUM(used."vaccinations unused")
FROM used
WHERE expires < '2021-04-12T11:10:06.473587Z';
  sum  
-------
 12662
(1 row)

vaccinations=# WITH used AS (
vaccinations(# SELECT orders.id, arrived, arrived + interval '30 days' AS "expires", injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
vaccinations(# injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
vaccinations(# FROM orders
vaccinations(# LEFT JOIN vaccinations ON orders.id = vaccinations.sourceBottle
vaccinations(# GROUP BY orders.id, orders.arrived, orders.injections
vaccinations(# )
vaccinations-# SELECT SUM(used."vaccinations unused")
vaccinations-# --SELECT id, DATE(arrived), expires ,injections, used."vaccinations used", used."vaccinations unused"
vaccinations-# FROM used
vaccinations-# WHERE expires < '2021-04-12T11:10:06.473587Z';
  sum  
-------
 12590
(1 row)
```

uvicorn main:app --reload

pytest app/tests/01_basic_tests.py

docker pull postgres