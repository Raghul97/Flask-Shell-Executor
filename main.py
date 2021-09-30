from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from utility.clone_repo import GitCLone
from celery import Celery
import os, time
from datetime import datetime
import subprocess

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

DOWNLOAD_FOLDER = './logs'
app.config['UPLOAD_FOLDER'] = DOWNLOAD_FOLDER

celery_app = Celery('main', broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

git_util = GitCLone()
git_util.clone()


@app.route('/')
def index():
    return render_template('index.html')


# celery Integration
@celery_app.task(bind=True)
def execute_shell(self, data):
    data = data["command_generated"].split(" ")
    data = data[1:]
    command = ['./repo/Run.sh']
    command.extend(data)
    try:
        current_date_time = datetime.now()
        os.system('chmod +x ./repo/Run.sh')
        with open("./logs/output-{}.txt".format(self.request.id), "w") as file:
            self.update_state(state='PROGRESS')
            subprocess.Popen(command, stdout=file, text=True)
            time.sleep(50)
    except Exception as err:
        self.update_state(state='FAILURE', meta={'message': "Error while executing shell script."})
        raise Exception(err)
    return {"message": "Task Execution Done!"}


@app.route('/form-parse', methods=["POST"])
def form_parse():
    response = request.get_json()
    task = execute_shell.apply_async(args=(response,))
    return jsonify({}), 202, {'Location': url_for('task_status',
                                                  task_id=task.id), 'taskid': task.id }


@app.route('/status/<task_id>')
def task_status(task_id):
    task = execute_shell.AsyncResult(task_id)
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


if __name__ == '__main__':
    app.run(debug=True)
