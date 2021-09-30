import os
from git import Repo


class GitCLone:
    def __init__(self):
        self.repo_url = "https://github.com/Raghul97/Dummy.git"
        self.clone_to_repo = "repo"

    def check_repo_free(self):
        if os.path.isdir(self.clone_to_repo):
            os.system('rm -rf repo')

    def clone(self):
        self.check_repo_free()
        Repo.clone_from(self.repo_url, self.clone_to_repo)
