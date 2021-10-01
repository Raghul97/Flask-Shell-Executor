import os
from git import Repo


class GitCLone:
    def __init__(self):
        self.repo_url = "https://github.com/Raghul97/Dummy.git"
        self.clone_to_repo = "/opt/repo"

    def check_repo_free(self):
        if os.path.isdir(self.clone_to_repo):
            os.system('rm -rf /opt/repo')

    def clone(self):
        '''
            clone the git repo, when the app is initialized.
        '''
        self.check_repo_free()
        Repo.clone_from(self.repo_url, self.clone_to_repo)
