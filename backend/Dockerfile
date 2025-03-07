# Use Python base image
FROM python:3.9-slim

COPY . /app/
WORKDIR /app/
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn uvicorn

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the FastAPI port
EXPOSE 8000

# Start Gunicorn with Uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
