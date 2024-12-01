# Use official Python image from DockerHub
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . /app/

# Expose the port that the app will run on
EXPOSE 8000

# Use Uvicorn to run the app (replace `app:app` with your module and app name)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
