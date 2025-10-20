FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --frozen

COPY . .

RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8080

CMD ["uv", "run", "python", "main.py"]
