# Base image (use a lightweight Python image)
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project files
COPY . .

# Expose port (if your app runs on 5000, for example)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
