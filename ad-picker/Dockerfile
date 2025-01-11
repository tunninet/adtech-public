# Use a lightweight Python 3.13 slim image as the base
FROM python:3.13-slim

# Set environment variable to prevent Python from buffering stdout and stderr
# Ensures logs are immediately visible in the console
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies from the requirements file
# --no-cache-dir ensures a smaller image by not caching intermediate files
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files and directories (e.g., app.py, gunicorn.conf.py, static/, etc.) into the container
COPY . /app

# Expose port 8080 to make it clear that the application will use this port
# This is helpful for documentation purposes, though not mandatory for container operation
EXPOSE 8080

# Define the command to run the application using Gunicorn
# Gunicorn is set to use a single worker process and bind to all network interfaces on port 8080
CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:8080", "app:app"]