# pull official base image
FROM python:3.8-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    curl `# для установки poetry` \
    git `# для установки зависимостей из git` \
    build-base  `# для сборки пакетов` \
    libffi-dev

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN mkdir /app
COPY pyproject.toml /app/
WORKDIR /app/
ARG POETRY_PARAMS
RUN poetry install $POETRY_PARAMS
COPY / /app/