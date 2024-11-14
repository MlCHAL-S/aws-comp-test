# Dockerfile for the backend server
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /app/

# Expose the Flask app port (default is 5000)
EXPOSE 5000

# Set the environment variable to disable interactive mode
ENV FLASK_ENV=production

# Run the Flask app
CMD ["python", "server.py"]
