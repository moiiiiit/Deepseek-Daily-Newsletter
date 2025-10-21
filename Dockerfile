# Use official Python image with version matching project requirement
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./
COPY . .

# Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Run tests and fail build if they do not pass
RUN poetry run pytest --maxfail=1 --disable-warnings

# Set entrypoint to main.py
CMD ["poetry", "run", "python", "main.py"]
