FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt

RUN chmod +x /app/server-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh