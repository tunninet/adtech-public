# Use a lightweight Python 3.13 image as the base
FROM python:3.13-slim

# Set environment variables
# Force kafka-python to use IPv4
ENV KAFKA_PYTHON_FORCE_IP_VERSION=4
# Prevent Python from buffering output to ensure logs are immediately visible
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file into the container
COPY requirements.txt .

# Install Python dependencies without using the cache for faster builds
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Kafka consumer script into the container
COPY consumer.py /app

# Specify the command to run the Kafka consumer script when the container starts
# Optionally, this could be wrapped with a process manager like Gunicorn
CMD ["python", "consumer.py"]