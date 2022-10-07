#!/bin/bash

# Bash script to start the flower ui server, when celery workers are
# up and running.
# Reference: https://testdriven.io/courses/django-celery/docker/#H-8-start-scripts

# set -o errexit
# set -o nounset

celery_is_up() {
    celery -A src inspect ping
}

until celery_is_up; do
    echo 'Celery workers starting...'
    sleep 1
done
    echo 'Celery workers now available, starting flower...'

celery -A src flower \
    --port=5555 \
    --auth_provider=flower.views.auth.GithubLoginHandler \
    --auth=${FLOWER_AUTH_EMAIL}