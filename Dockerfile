# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies required to compile the code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Compile your code
RUN pylint **/*.py
RUN mypy **/*.py
RUN bandit -r .

# Define command to run your application (if applicable)
CMD ["python3", "app.py"]
