# Python 3.12 Dev Container
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install devtools
RUN pip install --upgrade pip && pip install devtools

# [Optional] Install additional OS packages
# RUN apt-get update && apt-get install -y <package-name>

# Set up a workspace folder
WORKDIR /workspaces/${REPO_NAME}