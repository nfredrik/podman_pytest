# Use an official Python runtime as a base image (change version as needed)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your project files into the container
#COPY . .

# Default command to run tests with pytest
#CMD ["pytest", "-v"]
