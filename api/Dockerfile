# Use an official Python runtime as a parent image
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
# remove expose port for cloud run execution


# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD gunicorn -b 0.0.0.0:${PORT:-5000} app:app
