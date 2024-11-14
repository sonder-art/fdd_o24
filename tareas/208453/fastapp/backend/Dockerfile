# Use a basic Python 3.8 image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy application files and requirements
COPY ./app /app
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port that FastAPI will use
EXPOSE 80

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]