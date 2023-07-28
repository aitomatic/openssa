# Use an official Python 3.10 runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /apps/kbase
WORKDIR /app

# Copy the current directory contents into the container at /apps/kbase 
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install your custom .whl package
RUN pip install --no-cache-dir dist/openssm-0.1.5-py3-none-any.whl

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["gunicorn", "kbase.app:app", "-b", "0.0.0.0:8080"]
