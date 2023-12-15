import json
import time
from importlib import import_module

from .Backends import Backends
from .Paths import Paths


class Update:
    DAY_SECONDS = 24 * 60 * 60
    WEEK_SECONDS = 7 * DAY_SECONDS
    MONTH_SECONDS = 30 * DAY_SECONDS

    def __init__(self, logger, config, backends):
        self.__logger = logger
        self.__config = config
        self.__backends = backends

        if not Paths.TIMESTAMP_PATH.exists():
            self.__logger.info("Creating timestamp file.")
            self.__create_timestamp()

        self.__timestamp = self.__get_timestamp()

    def initiate(self):
        confirm_unstable = self.__config["logger"]["confirm_unstable"]
        branch_name = self.__config["updates"]["branch_name"]
        search_frequency = self.__config["updates"]["search_frequency"].lower()
        time_difference = time.time() - self.__timestamp["timestamp"]

        valid_frequencies = {
            "always": True,
            "day": time_difference >= self.DAY_SECONDS,
            "week": time_difference >= self.WEEK_SECONDS,
            "month": time_difference >= self.MONTH_SECONDS,
            "never": False
        }

        if not confirm_unstable and branch_name == "main" and search_frequency != "never":
            self.__logger.warning_unstable_branch(branch_name)

        if self.__backends[Backends.GIT]:
            if Paths.GIT_PATH.exists() and Paths.GIT_PATH.is_dir():
                repo = self.__repo()

                self.__checkout(repo, branch_name)

                try:
                    update_scheduled = valid_frequencies[search_frequency]

                    if update_scheduled:
                        self.__pull(repo, branch_name)
                except KeyError:
                    self.__logger.error(f"Unknown update frequency - {search_frequency}, available: {list(valid_frequencies.keys())}")
            else:
                self.__logger.error("Update canceled because Allor is not a git repository.")
        else:
            self.__logger.error("Update canceled because GitPython is not installed.")

    def __get_timestamp(self):
        with open(Paths.TIMESTAMP_PATH, "r") as f:
            return json.load(f)

    def __create_timestamp(self):
        with open(Paths.TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": 0}, f, ensure_ascii=False, indent=4)

    def __update_timestamp(self):
        with open(Paths.TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": time.time()}, f, ensure_ascii=False, indent=4)

    def __repo(self):
        git = import_module("git")
        repo = git.Repo

        return repo(Paths.ROOT_PATH, odbt=git.db.GitDB)

    def __checkout(self, repo, branch_name):
        from git import GitCommandError

        if repo.active_branch.name != branch_name:
            if any([branch.name == branch_name for branch in repo.branches]):
                try:
                    update_mode = self.__config["updates"]["update_mode"].lower()
                    valid_modes = ["soft", "hard"]

                    if update_mode == "soft":
                        repo.git.checkout(branch_name)
                    elif update_mode == "hard":
                        repo.git.checkout(branch_name, force=True)
                    else:
                        self.__logger.error(f"Unknown update mode - {update_mode}, available: {valid_modes}")
                except GitCommandError:
                    self.__logger.error(f"An error occurred while switching to the branch {branch_name}.")
            else:
                self.__logger.error(f"Branch with name {branch_name} not exist.")

    def __pull(self, repo, branch_name):
        from git import GitCommandError

        try:
            repo.remotes.origin.fetch()

            local_commits = list(repo.iter_commits(branch_name))[::-1]
            remote_commits = list(repo.iter_commits(f"origin/{branch_name}"))[::-1]

            incorrect_hex = any(lc != rc for lc, rc in zip(local_commits, remote_commits))

            if incorrect_hex:
                new_remote_commits = []
            else:
                last_hex = next((i for i, (lc, rc) in enumerate(zip(local_commits, remote_commits)) if lc != rc), len(local_commits))
                new_remote_commits = remote_commits[last_hex:] if len(remote_commits) > len(local_commits) else []

            if incorrect_hex or new_remote_commits:
                if self.__config["updates"]["install_update"]:
                    update_mode = self.__config["updates"]["update_mode"].lower()
                    valid_modes = ["soft", "hard"]

                    if update_mode == "soft":
                        if incorrect_hex:
                            self.__logger.warn("Incorrect hex of commits found in commits repository history.\n"
                                               "Updating using \"soft\" update mode is unlikely to complete successfully.")

                        repo.git.pull()
                    elif update_mode == "hard":
                        repo.git.reset('--hard', 'origin/' + branch_name)
                    else:
                        self.__logger.error(f"Unknown update mode - {update_mode}, available: {valid_modes}")

                        return

                    self.__update_timestamp()
                    self.__logger.info("Updates installed successfully.", self.__config["logger"]["install_complete"])
        except GitCommandError:
            self.__logger.error("An error occurred during the updating.\n"
                                "It is recommended to use \"hard\" update mode.\n"
                                "But be careful, it erases all personal changes from Allor repository.")
