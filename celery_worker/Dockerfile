FROM python:3.8-slim

# creating folder for cloning and logs.
RUN mkdir /opt/repo
RUN mkdir /opt/logs

# updating package and installing git.
RUN apt-get update
RUN apt-get -y install git
RUN git clone https://github.com/Raghul97/Dummy.git /opt/repo

# installing required packages in the container.
COPY requirements.freeze /
RUN pip install -r /requirements.freeze

ADD . /celery_worker
WORKDIR /celery_worker

# executing celery worker with taskname and celery app name.
ENTRYPOINT celery -A tasks.app worker --loglevel=info
