FROM python:3.11

# set work directory

RUN mkdir /armadion

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
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /armadion/entrypoint.sh
RUN chmod +x /armadion/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/armadion/entrypoint.sh"]