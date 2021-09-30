FROM python:3.8-slim

COPY requirements.freeze /
RUN pip install -r /requirements.freeze

ADD . /celery_worker
WORKDIR /celery_worker

ENTRYPOINT celery -A tasks.app worker --loglevel=info
