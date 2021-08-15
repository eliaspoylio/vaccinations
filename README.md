# Vaccination exercise

Assignment based on:
https://github.com/solita/vaccine-exercise-2021

Live version:
https://eliaspoyliovaccinations.herokuapp.com/

## Requirements to run locally

- Docker
- NodeJS (for Cypress testing)

## Get started

Create `.env` file in the project root. Replace `<USERNAME>` and `<PASSWORD>`:
```
POSTGRES_USER=<USERNAME>
POSTGRES_PASSWORD=<PASSWORD>
POSTGRES_URL=postgres:5432
POSTGRES_DB=vaccinations
```

Create `frontend/.env` file:
```
VUE_APP_API_URI=http://localhost:8080
```

In project root run docker compose:
`docker-compose --env-file .env up --build`

## Docs

Swagger docs created by FastAPI: http://127.0.0.1:8080/docs

## Testing

### Backend

To run Starlette Test Client in backend container, run in in the project root:

`chmod 777 test.sh`

`./test.sh`

### Frontend

To run Cypress test suite locally, run in `/frontend` folder:

`npm install`

`npm run test:e2e`


## Shutting down

Shut docker down with:
`docker-compose down`

