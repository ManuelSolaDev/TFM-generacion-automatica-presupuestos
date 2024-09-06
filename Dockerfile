# Use the official Python base image
FROM python:3.12.5

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Set the entrypoint command to launch the application
CMD ["python", "-m", "app.app"]