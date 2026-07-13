# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure stdout/stderr are unbuffered.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if needed, e.g., for sqlite3 or compilation)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Ensure the uploads directory exists
RUN mkdir -p /app/uploads

# Expose port 5000 for the app (Gunicorn)
EXPOSE 5000

# Define the command to run your app using Gunicorn
# 'app:app' assumes your Flask instance is named 'app' inside 'app.py'
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "app:app"]
