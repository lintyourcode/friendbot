FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.8.3

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "python", "-m", "friendbot"]
