FROM python:3.11-slim-buster

RUN mkdir -p /app/

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY config/ /app/config
COPY backend/ /app/backend

WORKDIR /app/