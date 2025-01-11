# Use a lightweight Python 3.13 image as the base
FROM python:3.13-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies listed in requirements.txt without using cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the seed_db.py script into the container's working directory
COPY seed_db.py /app/

# Set the default command to execute the seeding script when the container starts
CMD ["python", "/app/seed_db.py"]