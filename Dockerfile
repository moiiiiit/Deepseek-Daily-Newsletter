# Use official Python image with version matching project requirement
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files, excluding .venv and .pytest_cache
COPY pyproject.toml ./
COPY . .
RUN rm -rf .venv .pytest_cache

# Copy and set executable for run_newsletter.sh
COPY scripts/run_newsletter.sh /app/run_newsletter
RUN chmod +x /app/run_newsletter

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --no-interaction --no-ansi --with dev

# Run tests and fail build if they do not pass
RUN poetry run pytest --maxfail=1 --disable-warnings

# Set entrypoint to main.py in the package
CMD ["poetry", "run", "python", "-m", "deepseek_daily_newsletter.main"]
