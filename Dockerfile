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

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "Purchaseproject.wsgi:application", "--bind", "0.0.0.0:8000"]
