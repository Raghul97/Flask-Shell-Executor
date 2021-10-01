from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from utility.clone_repo import GitCLone
from celery import Celery
import os, time
import subprocess

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

# creating log folder if it does not exist already in the host.
DOWNLOAD_FOLDER = './logs'
if not os.path.isdir(DOWNLOAD_FOLDER):
    os.system('mkdir ./logs')

# adding log folder has upload folder to retireve logs when download request is sent.
app.config['UPLOAD_FOLDER'] = DOWNLOAD_FOLDER

# configuring celery to use redis as broker and backend. if running without docker compose, change the url to 'redis://redis:6379/0' to 'redis://localhost:6379/0'.
celery_app = Celery('main', broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

# cloning the required repositories.
git_util = GitCLone()
git_util.clone()


@app.route('/')
def index():
    return render_template('index.html')


# celery task for running shell script and create unique log file.
@celery_app.task(bind=True)
def execute_shell(self, data):
    data = data["command_generated"].split(" ")
    data = data[1:]
    command = ['./repo/Run.sh']
    # add arguments to be passed to the shell script.
    command.extend(data)
    try:
        # adding executable permission to shell script.
        os.system('chmod +x ./repo/Run.sh')
        with open("./logs/output-{}.txt".format(self.request.id), "w") as file:
            self.update_state(state='PROGRESS')
            # running shell script and redirecting the stdout to log file with unique task id.
            subprocess.Popen(command, stdout=file, text=True)
            time.sleep(50)
    except Exception as err:
        self.update_state(state='FAILURE', meta={'message': "Error while executing shell script."})
        raise Exception(err)
    return {"message": "Task Execution Done!"}


# parse the form data sent from client and execute the shell script asynchronous.
@app.route('/form-parse', methods=["POST"])
def form_parse():
    response = request.get_json()

    # execute_shell task is triggered with the form data using redis broker.
    task = execute_shell.apply_async(args=(response,))
    
    # send back feedback and task id to client as task executed successfully, so that client does not want to wait until the process gets completed.
    return jsonify({}), 202, {'Location': url_for('task_status',
                                                  task_id=task.id), 'taskid': task.id }


# get update on the status of task to get notified when the download is available.
@app.route('/status/<task_id>')
def task_status(task_id):

    # get result of the task with task id.
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


# if task state is success, send the file as attachment to client.
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
