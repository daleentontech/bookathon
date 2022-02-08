FROM python:3

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /client_api/requirements.txt
RUN pip install --no-cache-dir -r ./client_api/requirements.txt

COPY ./client_api /client_api
WORKDIR /client_api