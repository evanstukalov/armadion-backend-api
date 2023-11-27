FROM python:3.11.4-slim-buster

RUN mkdir /armadion && mkdir /armadion/staticfiles && mkdir /armadion/logs

WORKDIR /armadion

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install system dependencies
RUN apt-get update && apt-get -y install netcat-openbsd nano

# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
COPY .env.prod .env

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker && chmod +x /start-celeryworker

# run entrypoint.sh
ENTRYPOINT ["/entrypoint"]