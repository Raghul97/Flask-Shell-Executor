FROM python:3.8-slim

RUN mkdir /opt/repo
RUN mkdir /opt/logs

RUN apt-get update
RUN apt-get -y install git
RUN git clone https://github.com/Raghul97/Dummy.git /opt/repo

COPY requirements.freeze /
RUN pip install -r /requirements.freeze

ADD . /celery_worker
WORKDIR /celery_worker

ENTRYPOINT celery -A tasks.app worker --loglevel=info
