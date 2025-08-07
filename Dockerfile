# Base image
FROM python:3.11-slim

# Install uv, a fast Python package installer and dependency manager
RUN pip install uv

# Set the working directory inside the container.
WORKDIR /wardrobe

# Copy all the project files into the container.
COPY . .

# Use uv sync to install dependencies from pyproject.toml
RUN uv sync

# Expose port for uvicorn
EXPOSE 8080

# Use uv run to execute the uvicorn command.
# This ensures uvicorn is found within the virtual environment created by uv.
CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]