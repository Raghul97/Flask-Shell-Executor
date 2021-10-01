FROM python:3.8-slim

# installing required packages in the container.
COPY requirements.freeze /
RUN pip install -r /requirements.freeze

# adding source code to the container.
ADD . /celery_worker
WORKDIR /celery_worker

# executing celery worker with taskname and celery app name.
ENTRYPOINT celery -A tasks.app worker --loglevel=info
