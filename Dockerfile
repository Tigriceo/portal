FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /iwbuy_service

WORKDIR /iwbuy_service

ADD . /iwbuy_service/

RUN pip install -r requirements.txt