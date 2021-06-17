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
```


uvicorn main:app --reload

pytest app/tests/01_basic_tests.py

docker pull postgres