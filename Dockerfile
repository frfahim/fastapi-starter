FROM python:3.10-slim-bullseye as build-stage

WORKDIR /tmp

COPY requirements.txt /tmp/

FROM python:3.10-slim-bullseye as run-stage

# Install system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc g++ curl procps net-tools tini

# Set up the Python environment
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install the project dependencies
COPY --from=build-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the project files
COPY . /app/

# Expose the application port
EXPOSE 8000
