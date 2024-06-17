# Backend
FROM python:3.10 as backend

ENV PYTHONUNBUFFERED 1

WORKDIR /
COPY . /public_api
RUN pip install --no-cache-dir -r /public_api/requirements.txt
EXPOSE 8090