FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file and .env file into the /app/scripts directory
COPY requirements.txt /app/scripts/
COPY .env /app/scripts/

# Copy the scripts folder into the /app/scripts directory
COPY scripts /app/scripts/

# Change the working directory to /app/scripts
WORKDIR /app/scripts

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# We ensure the container stays running indefinitely, allowing us to execute commands in it as needed.
CMD ["tail", "-f", "/dev/null"]
