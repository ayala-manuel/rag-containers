FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
CMD ["uvicorn", "embeddings_service.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
