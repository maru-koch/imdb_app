FROM python:3.9-alpine

WORKDIR /core

RUN apk update \
    && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq

COPY ./requirements.txt /core/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./main.py /core/main.py
COPY ./workers /core/workers

RUN pip install --no-cache-dir --update -r /core/requirements.txt

CMD ["python", "main.py"]