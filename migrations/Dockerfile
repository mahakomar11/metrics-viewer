FROM python:3.11-slim-buster

RUN mkdir -p /app/
COPY migrations/requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend/database/models.py /app/backend/database/models.py
COPY config/ /app/config
COPY alembic.ini /app/alembic.ini
COPY migrations/alembic/ /app/migrations/alembic

WORKDIR /app/
