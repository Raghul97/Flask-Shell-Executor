FROM python:3.8-slim

# updating package and installing git.
RUN apt-get update
RUN apt-get -y install git

# creating folder for cloning and logs.
RUN mkdir /opt/repo
RUN mkdir /opt/logs

# installing required packages.
COPY requirements.freeze /
RUN pip install -r /requirements.freeze

ADD . /flask_app
WORKDIR /flask_app

# setting required environment.
ENV FLASK_ENV=development
ENV FLASK_APP=app.py

CMD flask run --host=0.0.0.0