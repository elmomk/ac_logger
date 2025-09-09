FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables with default values
ENV BACKEND_URL="http://backend:8000/metrics/temperature"
ENV SEND_INTERVAL=10

# Run the fake sensor
CMD ["python", "main.py"]
