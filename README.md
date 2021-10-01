# Flask Shell Executor - Dockerized app.

Flask Application for providing arguments to the shell script and attach the output file as downloadable from UI.

## Structure
.
├── celery_worker
│   ├── Dockerfile
│   ├── requirements.freeze
│   └── tasks.py
├── docker-compose.yml
├── flask_app
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.freeze
│   ├── static
│   │   ├── scripts
│   │   │   └── index.js
│   │   └── styles
│   │       └── index.css
│   ├── templates
│   │   └── index.html
│   └── utility
│       ├── clone_repo.py
│       └── __init__.py
└── README.md

7 directories, 13 files

## Procedure

#### Steps:

1. install docker.
    1. sudo apt-get update
    2. sudo apt install docker.io
    3. sudo systemctl start docker
    4. sudo systemctl enable docker
    5. check version: docker --version

2. Run the application.
    1. As it is docker application, flask_app, redis and celery_worker is run at same time.
        1. Run "docker-compose up" at root directory.

### Precaution:

1. make sure redis is not running in host. if it is running use:
    1. sudo systemctl stop redis

## File:

1. app.py - flask application configured with celery to use redis as message broker.

2. tasks.py - celery task that executes asynchoronously and sends back the task status with the help of messaging queue(redis).