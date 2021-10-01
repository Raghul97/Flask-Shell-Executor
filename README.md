# Flask Shell Executor

Flask Application for providing arguments to the shell script and attach the output file as downloadable from UI.

## Structure
.
├── main.py
├── README.md
├── requirements.freeze
├── static
│   ├── scripts
│   │   └── index.js
│   └── styles
│       └── index.css
├── templates
│   └── index.html
└── utility
    ├── clone_repo.py
    └── __init__.py

5 directories, 8 files

## Procedure

#### Steps:

1. create virtual environment.
    1. python3 -m venv venv
    2. source ,/venv/bin/activate

2.  install required packages.
    1. pip install -r requirements.freeze

3. install redis.
    1. sudo apt update
    2. sudo apt install redis-server
    3. sudo nano /etc/redis/redis.conf
    4. convert it to "supervised systemd"
    5. sudo systemctl restart redis.service
    6. check status: sudo systemctl status redis

3. run the application.
    1. python main.py

## File:

1. main.py - flask application configured with celery to use redis as message broker.
2. clone_repo.py - module for cloning the required projects.
