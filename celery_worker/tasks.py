import os, subprocess, time
from celery import Celery, states
from celery.utils.log import get_task_logger
from celery.exceptions import Ignore

# setting up logger for celery.
logger = get_task_logger(__name__)

# config celery to use redis broker as backend queue.
app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


# celery task for running shell script and create unique log file.
@app.task(bind=True)
def execute_shell(self, data):
    logger.info('Got Request - Starting work ')
    data = data["command_generated"].split(" ")
    data = data[1:]
    command = ['/opt/repo/Run.sh']
    # add arguments to be passed to the shell script.
    command.extend(data)
    try:
        # adding executable permission to shell script.
        os.system('chmod +x /opt/repo/Run.sh')
        with open("/opt/logs/output-{}.txt".format(self.request.id), "w") as file:
            self.update_state(state='PROGRESS')
            # running shell script and redirecting the stdout to log file with unique task id.
            subprocess.Popen(command, stdout=file, text=True)
            time.sleep(50)
            logger.info('Work Finished Successfully')
    except Exception as err:
        self.update_state(state=states.FAILURE, meta={'message': "Error while executing shell script."})
        logger.info('Work Finished Unsuccessfully')
        raise Ignore()
    return {"message": "Task Execution Done!"}
    