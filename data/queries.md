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

-------------
SELECT orders.id, orders.injections, COUNT(vaccinations.sourceBottle) AS "vaccinations used",
orders.injections - COUNT(vaccinations.sourceBottle) AS "vaccinations unused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
WHERE vaccinations.vaccinationDate < '2021-01-05' 
GROUP BY orders.id, orders.injections;

WITH injectionsused AS (
SELECT orders.id, orders.injections, COUNT(vaccinations.sourceBottle) AS "vused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
WHERE vaccinations.vaccinationDate < '2021-01-05' 
GROUP BY orders.id, orders.injections
)
SELECT SUM(vused)
FROM injectionsused;

---------------
WITH injectionsused AS (
SELECT orders.id, arrived + interval '30 days' AS "expires", orders.injections - COUNT(vaccinations.sourceBottle) AS "vunused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
WHERE vaccinations.vaccinationDate <= '2021-04-12T11:10:06.473587Z'
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT SUM(vunused)
FROM injectionsused
WHERE expires > '2021-04-12T11:10:06.473587Z';
---------------
WITH injectionsused AS (
SELECT orders.id, arrived + interval '30 days' AS "expires", orders.injections - COUNT(vaccinations.sourceBottle) AS "vunused"
FROM orders
INNER JOIN vaccinations ON orders.id = vaccinations.sourceBottle
WHERE vaccinations.vaccinationDate <= '20210223'
GROUP BY orders.id, orders.arrived, orders.injections
)
SELECT SUM(vunused)
FROM injectionsused
WHERE expires < DATE('20210223') + interval '10' day AND expires > '20210223';
------------
SELECT
date_trunc('day', arrived) AS "day",
count(orders.id) AS "orders",
sum(injections) AS "injections",
count(vaccinations.id) AS "vaccinations"
FROM orders
FULL OUTER JOIN vaccinations ON orders.arrived=date_trunc('day', vaccinations.vaccinationDate)
GROUP BY day
ORDER BY day;
--------------
WITH ordates AS (
  SELECT
  date_trunc('day', arrived) AS "day",
  count(orders.id) AS "orders",
  sum(injections) AS "injections"
  FROM orders
  GROUP BY day
)

SELECT 
ordates.day,
ordates.orders,
ordates.injections,
count(vaccinations.id) AS "vaccinations" 
FROM ordates
FULL OUTER JOIN vaccinations ON ordates.day=date_trunc('day', vaccinations.vaccinationDate)
GROUP BY day, ordates.orders, ordates.injections
ORDER BY day;

SELECT sum(ordates.orders) FROM ordates;
```

