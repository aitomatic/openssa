# docker file for a openssa with ollama environment
# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory
WORKDIR /openssa

# Install git and any other system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends git=1:2.39.5-0+deb12u1 && rm -rf /var/lib/apt/lists/*
RUN pip install Poetry --upgrade 
# Copy the requirements file and install dependencies
COPY . /openssa/
# RUN pip install --no-cache-dir -r requirements.txt


# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
