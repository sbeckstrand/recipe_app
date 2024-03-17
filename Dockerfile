# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pipenv
RUN pip install pipenv

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install dependencies using pipenv
RUN pipenv install --deploy --system

# Copy the Django application code into the container
COPY . /app/

# Make migrations
RUN python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run the Django application
python manage.py runserver 0.0.0.0:8000
