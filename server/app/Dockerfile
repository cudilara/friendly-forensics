# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /easy_forensics/server/app/
WORKDIR /easy_forensics/server/app/

# Copy the current directory contents into the container at /easy_forensics/server/app/
#ADD . /easy_forensics/server/app/docker
ADD . .
COPY requirements.txt /easy_forensics/server/app/
WORKDIR /easy_forensics/server/app/
RUN pip install -r requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Define environment variable
ENV NAME WebserverDocker

# Run app.py when the container launches
#CMD [cd .. & 'python', "webserver.py"]
ENTRYPOINT ./webserver.py