# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
	curl build-essential pkg-config libhdf5-dev \
	&& rm -rf /var/lib/apt/lists/*

# Copy only necessary files to install deps quickly
COPY Pipfile Pipfile.lock ./

# Install pipenv and deps
RUN pip install --no-cache-dir pipenv && \
	PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile

# Copy simulator code
COPY simulator ./simulator

# Expose port
EXPOSE 8000

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD curl -f http://127.0.0.1:8000/ || exit 1

# Run with python -m uvicorn to avoid path issues
CMD ["pipenv","run","python","-m","uvicorn","simulator.v2.backend.main:app","--host","0.0.0.0","--port","8000"]
