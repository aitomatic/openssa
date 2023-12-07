# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /apps/chatssm
WORKDIR /app

# Copy the current directory contents into the container at /apps/chatssm 
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["gunicorn", "chatssm.app:app", "-b", "0.0.0.0:8080"]
