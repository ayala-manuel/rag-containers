# api/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copia las carpetas necesarias
COPY ./api /app/api
COPY ./core /app/core
COPY ./utils /app/utils

COPY ./api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
