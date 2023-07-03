ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

WORKDIR /jwt

RUN apt-get update && pip install poetry && poetry config virtualenvs.create false
RUN pip install --upgrade --no-cache pip

COPY ./pyproject.toml /jwt/
COPY ./poetry.lock /jwt/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache -r ./requirements.txt

COPY ./jwt_service /jwt/jwt_service


ENTRYPOINT uvicorn jwt_service.main:app --host 0.0.0.0 --port 8082 --reload
