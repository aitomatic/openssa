FROM --platform=linux/amd64 python:3.12-slim AS base

# Install Poetry
RUN apt update -y && apt upgrade -y && apt install git -y
RUN apt update -y && apt install poppler-utils -y
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir poetry==1.3.2


RUN poetry config virtualenvs.in-project true && \
    poetry config installer.max-workers 10

WORKDIR /api

COPY pyproject.toml poetry.lock /api/

# =======================================
# Build image
FROM base AS build
ENV POETRY_REQUESTS_TIMEOUT=300
ENV PIP_DEFAULT_TIMEOUT=300
RUN poetry install

# =======================================
# App image
FROM base AS app

COPY --from=build /api/.venv /api/.venv

ENV PATH="/api/.venv/bin:$PATH"
ENV PATH="/api:$PATH"
# ENV PATH="/api/openssa:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/"

COPY . /api/

EXPOSE 8080

CMD ["sh", "start.sh"]
