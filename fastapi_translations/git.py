import datetime

from git import Repo


class FastAPIGitDocs:

    def __init__(self) -> None:
        self.repo = Repo(".")

    def get_commit_date_for(self, file: str) -> datetime.datetime | None:
        commits = list(self.repo.iter_commits(paths=file, max_count=1))
        if commits:
            return commits[0].committed_datetime

        return None
