# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
