FROM mcr.microsoft.com/mirror/docker/library/python:3.11-slim as builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY ./pyproject.toml ./poetry.lock ./
# poetry needs a README.md to build the project
RUN touch README.md 

RUN poetry install && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN mkdir outputs
COPY prompts/ prompts
COPY *.py .
COPY *.png .

EXPOSE 8080

CMD ["gradio", "app.py"]