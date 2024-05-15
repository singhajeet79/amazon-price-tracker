# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any dependencies required to compile the code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install type stubs for requests and bs4 modules
RUN python -m pip install types-requests types-beautifulsoup4

# Install pylint
RUN pip install pylint
RUN pip install mypy

# Compile your code
RUN pylint **/*.py
RUN mypy */*.py
RUN bandit -r .

# Define command to run your application (if applicable)
CMD ["python3", "app.py"]
