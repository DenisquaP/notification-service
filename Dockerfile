FROM python:3.10

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .
COPY .env .

RUN pip install -r requirements.txt

COPY ./app /code