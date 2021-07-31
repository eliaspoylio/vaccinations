# Vaccination exercise

https://github.com/solita/vaccine-exercise-2021

Create `.env` file:
```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_URL=postgres:5432
POSTGRES_DB=vaccinations
```

Create `frontend/.env` file:
```
VUE_APP_API_URI=localhost:8080
``` 
`docker-compose --env-file .env up --build`

`chmod 777 test.sh`
`chmod 777 psql.sh`

`docker-compose down`