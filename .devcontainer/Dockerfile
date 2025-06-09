FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Install any extra system dependencies you need here
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# (Optional) Add more system dependencies below as needed

# Copy requirements file first to leverage Docker cache
COPY requirements-dev.txt /tmp/pip-tmp/

# Install Python development tools
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt \
    && rm -rf /tmp/pip-tmp

# Set working directory
WORKDIR /workspace 