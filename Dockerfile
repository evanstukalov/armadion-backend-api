FROM python:3.11.4-slim-buster

# set work directory

RUN mkdir /armadion && mkdir /armadion/staticfiles

WORKDIR /armadion

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install system dependencies
RUN apt-get update && apt-get -y install netcat-openbsd

# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . .

RUN sed -i 's/\r$//g' /armadion/scripts/entrypoint.sh && chmod +x /armadion/scripts/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/armadion/scripts/entrypoint.sh"]