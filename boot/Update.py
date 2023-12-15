import json
import time

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

        if not Paths.CONFIG_PATH.exists():
            self.__logger.info("Creating timestamp file.")
            self.__create_timestamp()

        self.__timestamp = self.__get_timestamp()

    def initiate(self):
        confirm_unstable_agreement = self.__config["logger"]["confirm_unstable"]
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

        try:
            it_is_time_for_update = valid_frequencies[search_frequency]
        except KeyError:
            self.__logger.error(f"Unknown update frequency - {search_frequency}, available: {list(valid_frequencies.keys())}")

            return

        if not confirm_unstable_agreement and branch_name == "main" and search_frequency != "never":
            self.__logger.warning_unstable_branch(branch_name)

        if it_is_time_for_update:
            if not (Paths.GIT_PATH.exists() and Paths.GIT_PATH.is_dir()):
                self.__logger.error("Root directory of Allor is not a git repository. Update canceled.")

                return

            self.__update_allor(branch_name)

    def __get_timestamp(self):
        with open(Paths.TIMESTAMP_PATH, "r") as f:
            return json.load(f)

    def __create_timestamp(self):
        with open(Paths.TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": 0}, f, ensure_ascii=False, indent=4)

    def __update_timestamp(self):
        with open(Paths.TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": time.time()}, f, ensure_ascii=False, indent=4)

    def __update_allor(self, branch_name):
        if self.__backends[Backends.GIT]:
            import git

            from git import Repo
            from git import GitCommandError

            # noinspection PyTypeChecker, PyUnboundLocalVariable
            repo = Repo(Paths.ROOT_PATH, odbt=git.db.GitDB)
            current_commit = repo.head.commit.hexsha

            repo.remotes.origin.fetch()

            latest_commit = getattr(repo.remotes.origin.refs, branch_name).commit.hexsha

            if current_commit == latest_commit:
                self.__logger.info("New updates not found.", self.__config["logger"]["updates_search"])
            else:
                self.__logger.info("New updates are available.", self.__config["logger"]["updates_search"])

                if self.__config["updates"]["install_update"]:
                    update_mode = self.__config["updates"]["update_mode"].lower()
                    valid_modes = ["soft", "hard"]

                    if repo.active_branch.name != branch_name:
                        try:
                            repo.git.checkout(branch_name)
                        except GitCommandError:
                            self.__logger.error(f"An error occurred while switching to the branch {branch_name}.")

                            return

                    if update_mode == "soft":
                        try:
                            repo.git.pull()
                        except GitCommandError:
                            self.__logger.error("An error occurred during the update. \n"
                                                "It is recommended to use \"hard\" update mode. \n"
                                                "But be careful, it erases all personal changes from Allor repository.")

                    elif update_mode == "hard":
                        repo.git.reset('--hard', 'origin/' + branch_name)
                    else:
                        self.__logger.error(f"Unknown update mode - {update_mode}, available: {valid_modes}")

                        return

                    self.__logger.info("Updates installed successfully.", self.__config["logger"]["install_complete"])

            self.__update_timestamp()
        else:
            self.__logger.error("Update canceled because GitPython is not installed.")
