FROM python:3.11.4-slim-buster

# set work directory

RUN mkdir /armadion
RUN mkdir /armadion/staticfiles

WORKDIR /armadion

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install system dependencies
RUN apt-get update && apt-get -y install netcat-openbsd

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY scripts/entrypoint.sh scripts/entrypoint.sh
RUN sed -i 's/\r$//g' /armadion/scripts/entrypoint.sh
RUN chmod +x /armadion/scripts/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/armadion/scripts/entrypoint.sh"]