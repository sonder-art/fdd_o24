# Use a basic Python 3.8 image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy application files and requirements
COPY ./app /app
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose Streamlit port (default 8501)
EXPOSE 8501

# Run the Streamlit application

CMD ["streamlit", "run", "/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]