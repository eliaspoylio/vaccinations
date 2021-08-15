# Vaccination exercise

Assignment based on:
https://github.com/solita/vaccine-exercise-2021

Live version:
https://eliaspoyliovaccinations.herokuapp.com/

## Requirements to run locally

- Docker
- NodeJS

## Get started

1. In `/frontend` run: `npm install -g @vue/cli`

2. In project root run docker compose: `docker-compose up --build`

## Testing

### Backend

To run pytest in backend container, run in in the project root:

`docker exec -t vaccinations_backend_1 pytest --color=auto`

### Frontend

To run Cypress test suite locally, run in `/frontend` folder:

`npm install`

`npm run test:e2e`


## Shutting down and cleaning up

Shut docker down with:
`docker-compose down`

Uninstall vue cli: `npm uninstall -g @vue/cli`

## Description



### Frontend

Vue3 app that displays data fetched from the backend in text and visualized form.

Dependencies:

Package | Usage
--------|------
axios   | GET-requests to backend
moment  | Date & time formatting
vue3-apexcharts | Data visualizations
vue3-datepicker | Allows to pick from valid dates

On mount: 
- app makes a request to "timeseries"
 endpoint
- the first and the last date from timeseries data are used to set min&max values to datepicker.
- data is used for drawing the timeseries line chart

When "Update dashboard" button is pushed a series of requests is made to backend using chosen date and time as parameter. Responses are set to an array and parts of it are used in main template and the rest are passed to components as props.

Cypress E2E test suite for basic functionality is included.

### Backend

FastAPI app that makes SQL queries to Postgres. SQLAlchemy is used as an ORM and psycopg2 as driver for connecting to Postgres. More complex queries are written in raw SQL, but queries are parameterized to protect the database from SQL injection.

Swagger docs created by FastAPI: http://127.0.0.1:8080/docs

Pytest test suite is provided to test API endpoints and that no extra characters can be written in queries.