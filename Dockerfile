FROM python:3.9-alpine

WORKDIR /core

COPY ./requirements.txt /core/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./app /core/app

RUN pip install --no-cache-dir --update -r /core/requirements.txt

CMD ["python", "app/main.py"]