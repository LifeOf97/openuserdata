#########################
# Base image
#########################
FROM python:3.10-slim-buster AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########################
# final build
#########################
FROM python:3.10-slim-buster

# update apt and install needed dependencies
RUN apt update && apt-get install -y netcat

# create system user/group
RUN useradd --create-home --shell /bin/bash --user-group realestkma

# update/upgrade pip
RUN pip install --upgrade pip

# activate system user
USER realestkma

# create needed directories
ENV HOME=/home/realestkma
ENV APP_HOME=$HOME/app
RUN mkdir $APP_HOME
RUN mkdir -p $APP_HOME/logs/gunicorn
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

# set working directory
WORKDIR $APP_HOME

# copy over required files from base image
COPY --from=builder --chown=realestkma:realestkma /app/wheels /wheels
COPY --from=builder --chown=realestkma:realestkma /app/requirements.txt .

# add dir to PATH
ENV PATH="${PATH}:${HOME}/.local/bin"

# install required app dependencies
RUN pip install --user --no-cache /wheels/*

# copy project over
COPY --chown=realestkma:realestkma . $APP_HOME

# run entrypoint script
ENTRYPOINT ["/home/realestkma/app/entrypoint.sh"]
