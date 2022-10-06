#########################
#####Base image
#########################
FROM python:3.10-slim-buster AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########################
## final build
#########################
FROM python:3.10-slim-buster

# update repo and install needed dependencies
RUN apt update && apt-get install -y python3-dev

# create system user/group
RUN useradd --create-home --shell /bin/bash --user-group justhighlight

# update/upgrade pip
RUN pip install --upgrade pip

# activate system user
USER justhighlight

# create needed directories
ENV HOME=/home/justhighlight
ENV APP_HOME=$HOME/backend
RUN mkdir $APP_HOME
RUN mkdir -p $APP_HOME/logs/gunicorn
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# copy over required dependencies
COPY --from=builder --chown=justhighlight:justhighlight /app/wheels /wheels
COPY --from=builder --chown=justhighlight:justhighlight /app/requirements.txt .

# add required dir to PATH
ENV PATH="${PATH}:${HOME}/.local/bin"

# install dependencies
RUN pip install --user --no-cache /wheels/*

# copy project over
COPY --chown=justhighlight:justhighlight . $APP_HOME

# CMD [ "gunicorn", "-b 0.0.0.0:8000", "src.wsgi:application" ]