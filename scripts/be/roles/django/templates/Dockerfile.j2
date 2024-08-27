# Copyright (c) 2024 Perpetuator LLC

# Build environment
FROM python:3.11-slim as production
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

# Install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copy pyproject.toml, thus we only rebuild the image when the pyproject.toml file changes from this point on
COPY pyproject.toml .

# Install Python dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the files
COPY . .

# Install npm dependencies and run build:css
#RUN npm install && \
#    npm run build:css

# Collect static files
RUN poetry run python manage.py collectstatic --no-input
