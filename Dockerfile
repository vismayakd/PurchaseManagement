# Use official Python image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Run collectstatic during build
RUN python manage.py collectstatic --noinput

# Give execution permissions to start.sh
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Start the application using start.sh
CMD ["./start.sh"]