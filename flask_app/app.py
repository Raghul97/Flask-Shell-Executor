from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from celery import Celery
import os

app = Flask(__name__)

# adding log folder has upload folder to retireve logs when download request is sent.
DOWNLOAD_FOLDER = '/opt/logs'
app.config['UPLOAD_FOLDER'] = DOWNLOAD_FOLDER

# configuring celery to use redis as broker and backend. if running without docker compose, change the url to 'redis://redis:6379/0' to 'redis://localhost:6379/0'.
celery_app = Celery('celery_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.route('/')
def index():
    return render_template('index.html')


# parse the form data sent from client and execute the shell script asynchronous.
@app.route('/form-parse', methods=["POST"])
def form_parse():
    response = request.get_json()

    # execute_shell task is triggered with the form data using redis broker.
    task = celery_app.send_task('tasks.execute_shell', kwargs={'data': response})

    # send back feedback and task id to client as task executed successfully, so that client does not want to wait until the process gets completed.
    return jsonify({}), 202, {'Location': url_for('task_status', task_id=task.id), 'taskid': task.id }


# get update on the status of task to get notified when the download is available.
@app.route('/status/<task_id>', methods=["GET"])
def task_status(task_id):

    # get result of the task with task id.
    task = celery_app.AsyncResult(task_id, app=celery_app)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
        }
    else:
        response = {
            'state': task.state,
            'message': "something went wrong."
        }
    return jsonify(response)


# if task state is success, send the file as attachment to client.
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)
