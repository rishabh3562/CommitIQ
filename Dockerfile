# Dockerfile

FROM python:3.10.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first to leverage Docker cache
COPY requirements.txt .


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install watchdog for hot-reloading
# RUN pip install watchdog

# Copy the rest of the application code
COPY . .

# Install make if not present
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

# Default command (overridden by docker-compose)
CMD ["python", "main.py"]

