FROM docker.io/library/python:3.9-slim

ENV PYTHONPATH /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY bin bin
COPY pybot pybot
COPY conf/pybot.conf conf/

ENTRYPOINT [ "bin/pybot" ]