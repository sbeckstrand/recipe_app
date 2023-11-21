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

# Copy the Nginx configuration file into the container
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Expose the port that Django runs on (default is 8000)
EXPOSE 8000

# Run Django migrations to create the database schema and apply changes
RUN python manage.py migrate

# Create a default superuser
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

