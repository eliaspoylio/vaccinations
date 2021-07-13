export $(grep -v '^#' .env | xargs)

docker exec -it vaccinations_postgres_1 psql -U $POSTGRES_USER -d vaccinations