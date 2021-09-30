FROM python:3.8-slim

RUN apt-get update
RUN apt-get -y install git

RUN mkdir /opt/repo
RUN mkdir /opt/logs

COPY requirements.freeze /
RUN pip install -r /requirements.freeze

ADD . /flask_app
WORKDIR /flask_app

ENV FLASK_ENV=development

ENV FLASK_APP=app.py

CMD flask run --host=0.0.0.0