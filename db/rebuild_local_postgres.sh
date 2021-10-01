#!/usr/bin/env bash

POSTGRES_VERSION=postgres:14.0-bullseye
POSTGRES_PORT=${POSTGRES_PORT}
DOCKER_CONTAINER_NAME=jbc-postgres

POSTGRES_INIT_FILE=db/postgres_v1.sql

if [ -z ${POSTGRES_PORT} ] ; then
    POSTGRES_PORT=5432
fi

running_short_hash=$(docker ps -a | grep ${DOCKER_CONTAINER_NAME} | awk '{print $1}')
if [ ! -z ${running_short_hash} ] ; then
    docker stop ${running_short_hash} &>/dev/null
    docker rm ${running_short_hash} &>/dev/null
fi

docker run \
    --name ${DOCKER_CONTAINER_NAME} \
    -e POSTGRES_PASSWORD=jbc \
    -e POSTGRES_USER=jbc \
    -e POSTGRES_DB=jbc \
    -p ${POSTGRES_PORT}:5432 \
    --restart=always \
    -d ${POSTGRES_VERSION} &>/dev/null

timeout 90s bash -c "until docker exec ${DOCKER_CONTAINER_NAME} pg_isready &>/dev/null; do sleep 5 ; done"

echo "Postgres is up!"

PGPASSWORD=jbc psql --dbname jbc --username jbc --port ${POSTGRES_PORT} --host localhost -f ${POSTGRES_INIT_FILE}