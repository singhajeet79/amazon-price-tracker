# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python -m pip install types-requests types-beautifulsoup4

# Copy the current directory contents into the container at /app
COPY . .

# Define command to run your application
CMD ["python3", "app.py"]

