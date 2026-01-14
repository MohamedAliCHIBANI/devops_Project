# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Expose the port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]