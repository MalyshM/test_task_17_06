# Backend
FROM python:3.10 as backend

ENV PYTHONUNBUFFERED 1

WORKDIR /
COPY . /private_api
RUN pip install --no-cache-dir -r /private_api/requirements.txt
EXPOSE 8090