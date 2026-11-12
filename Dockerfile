# Use the official Python base image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure stdout/stderr are unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local app directory into the container
# Note: For local development, docker-compose uses a volume mount to override this,
# allowing for hot-reloading without rebuilding the image.
COPY ./app /app

# The command to run the API (also overridden by docker-compose for dev mode)
CMD ["uvicorn", "app_main:app", "--host", "0.0.0.0", "--port", "8000"]