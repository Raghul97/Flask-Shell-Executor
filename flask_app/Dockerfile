FROM python:3.8-slim

# installing required packages.
COPY requirements.freeze /
RUN pip install -r /requirements.freeze

ADD . /flask_app
WORKDIR /flask_app

# setting required environment.
ENV FLASK_ENV=development
ENV FLASK_APP=app.py

CMD flask run --host=0.0.0.0