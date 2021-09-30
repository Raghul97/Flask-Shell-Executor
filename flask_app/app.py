from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from utility.clone_repo import GitCLone
from celery import Celery
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = '/opt/logs'
if not os.path.isdir(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = DOWNLOAD_FOLDER

celery_app = Celery('celery_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

git_util = GitCLone()
git_util.clone()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form-parse', methods=["POST"])
def form_parse():
    response = request.get_json()
    task = celery_app.send_task('tasks.execute_shell', kwargs={'data': response})
    return jsonify({}), 202, {'Location': url_for('task_status', task_id=task.id), 'taskid': task.id }


@app.route('/status/<task_id>')
def task_status(task_id):
    task = celery_app.AsyncResult(task_id, app=celery_app)
    print(task.state)
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


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)

