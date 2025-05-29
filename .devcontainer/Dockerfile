FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - \
    && sudo apt-get install -y nodejs

# Install additional tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.dev.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.dev.txt

# Create workspace directory
RUN mkdir -p /workspace
WORKDIR /workspace

# Set up user
USER vscode
