# Build stage
FROM python:3.14-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables for uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy source and install project
COPY . .
RUN uv sync --frozen --no-dev --no-editable

# Runtime stage
FROM python:3.14-slim-bookworm AS runtime

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source code
WORKDIR /app
COPY src /app/src

# Create a non-root user
RUN groupadd -r app && useradd -r -g app app && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
