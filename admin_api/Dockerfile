FROM python:3

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /admin_api/requirements.txt
RUN pip install --no-cache-dir -r ./admin_api/requirements.txt

COPY ./admin_api /admin_api
WORKDIR /admin_api