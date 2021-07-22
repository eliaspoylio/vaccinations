# Vaccination exercise

https://github.com/solita/vaccine-exercise-2021

Create `.env` file:
```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_URL=postgres:5432
POSTGRES_DB=vaccinations
```
`docker-compose --env-file .env up --build`

`chmod 777 test.sh`
`chmod 777 psql.sh`

`docker-compose down`