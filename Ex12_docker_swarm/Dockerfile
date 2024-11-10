# Base image
FROM python:3.10-slim

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . /app

# Ensure the instance directory exists
RUN mkdir -p instance

# Run setup.py to initialize the database
RUN python setup.py

# Expose the port Flask will run on
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production  

# Start the Flask app using Flask CLI
CMD ["flask", "run", "--host=0.0.0.0"]

