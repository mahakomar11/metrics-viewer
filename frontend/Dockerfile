FROM python:3.11-slim-buster

RUN mkdir -p /app/

COPY frontend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY frontend/ /app/frontend

WORKDIR /app/