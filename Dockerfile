# 1. Base Stage (Common Setup)
FROM python:3.14-slim-bookworm AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /app

# 2. Builder Stage (Install ALL dependencies including DEV for tests)
FROM base AS testing
COPY pyproject.toml uv.lock ./
# REMOVED: --no-dev. We NEED dev dependencies (pytest) here.
RUN uv sync --frozen --no-install-project 
COPY . .
RUN uv sync --frozen --no-editable

# 3. Production Builder (Install ONLY production dependencies)
FROM base AS prod-builder
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev
COPY . .
RUN uv sync --frozen --no-dev --no-editable


# 4. Runtime Stage (Final Production Image)
FROM python:3.14-slim-bookworm AS runtime
COPY --from=prod-builder /app/.venv /app/.venv
WORKDIR /app
COPY src /app/src
RUN groupadd -r app && useradd -r -g app app && chown -R app:app /app
USER app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]