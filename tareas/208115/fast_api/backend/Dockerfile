FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application file
COPY main.py .

# Use an absolute import in CMD
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]





