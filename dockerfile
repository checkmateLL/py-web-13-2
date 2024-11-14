# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    iputils-ping \
    net-tools \
    wait-for-it

# Install Poetry
RUN pip install poetry

# Copy the project dependency files
COPY pyproject.toml poetry.lock /app/

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install

# Copy the wait-for-it.sh script and set permissions
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Copy the entire project
COPY . /app

# Expose port 8000 for Django
EXPOSE 8000

# Run the application
CMD ["wait-for-it", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
