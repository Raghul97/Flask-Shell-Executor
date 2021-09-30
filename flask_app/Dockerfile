FROM python:3.8-slim

COPY requirements.freeze /
RUN pip install -r /requirements.freeze

ADD . /flask_app
WORKDIR /flask_app

ENV FLASK_ENV=development

ENV FLASK_APP=app.py

CMD flask run --host=0.0.0.0