#! /bin/bash

PGPASSWORD='password' echo 'DELETE FROM menu; DELETE FROM submenu; DELETE FROM dish;' | psql -U postgres -d data;

docker stop 1homework-homework-1-postgres-1; docker container rm 1homework-homework-1-postgres-1;
docker-compose up -d;
source ./venv/scripts/activate
uvicorn app.main:app --reload;

