# Use Ubuntu base image with Python
FROM ubuntu:22.04

# Set environment variables for non-interactive apt installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python3 as default python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates/ ./templates/

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port 5000 for the web app
EXPOSE 5000

# Set the command to run the Flask application
CMD ["python3", "app.py"]