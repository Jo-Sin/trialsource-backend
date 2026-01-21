# syntax=docker.io/docker/dockerfile:1.7-labs

FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY --exclude=.env* --exclude=dev-* . .
COPY ./.env.prod /app/.env
RUN pip install -r requirements.txt

RUN chmod +x /app/entrypoint-server.sh
RUN chmod +x /app/entrypoint-celery-worker.sh
RUN chmod +x /app/entrypoint-celery-beat.sh