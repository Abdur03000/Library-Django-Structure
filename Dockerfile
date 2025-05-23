FROM python:3.7.9-buster

ENV PYTHONUNBUFFERED=1

# Install curl (if not installed) and Poetry
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry (latest recommended method, since your script is deprecated)
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy only dependency files first for caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies (this creates a virtualenv inside /app/.venv)
RUN poetry config virtualenvs.in-project true \
 && poetry install --no-root --no-interaction --no-ansi

# Copy app code
COPY . /app

# Set environment variable to use Poetry virtualenv
ENV PATH="/app/.venv/bin:$PATH"

# Expose port 8080 (Fly.io default)
EXPOSE 8080

# Run uvicorn inside the "Library" folder on port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
