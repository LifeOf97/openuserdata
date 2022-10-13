#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres to start..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started successfully"
fi

exec "$@"