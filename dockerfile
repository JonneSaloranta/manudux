FROM python:3.11-bookworm

# Update system packages
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# Environment variable
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create and set up working directory
RUN mkdir /var/manudux
WORKDIR /var/manudux

# Install dependencies
COPY requirements.txt /var/manudux/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /var/manudux/

# Ensure the non-root user has ownership of all necessary files, including volumes
RUN chown -R myuser:myuser /var/manudux/

# Switch to non-root user
USER myuser

# Entrypoint for the container
ENTRYPOINT ["/bin/sh", "/var/manudux/runserver.sh"]
