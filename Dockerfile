FROM python:3.12.4
LABEL authors="denom"

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt