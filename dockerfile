# Use an official Python runtime as a parent image
FROM python:3.9-slim


# Install build dependencies
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install  -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

