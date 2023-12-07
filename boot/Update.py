import json
import time

from .Constants import Constants
from .Logger import Logger


class Update:
    def __init__(self, config):
        self.__logger = Logger()
        self.__config = config

        if not Constants.CONFIG_PATH.exists():
            self.__logger.info("Creating timestamp file.")
            self.__create_timestamp()

        self.__timestamp = self.__get_timestamp()

    def initiate(self):
        confirm_unstable_agreement = self.__config["updates"]["confirm_unstable"]
        branch_name = self.__config["updates"]["branch_name"]
        update_frequency = self.__config["updates"]["update_frequency"].lower()
        time_difference = time.time() - self.__timestamp["timestamp"]

        valid_frequencies = {
            "always": True,
            "day": time_difference >= Constants.DAY_SECONDS,
            "week": time_difference >= Constants.WEEK_SECONDS,
            "month": time_difference >= Constants.MONTH_SECONDS,
            "never": False
        }

        try:
            it_is_time_for_update = valid_frequencies[update_frequency]
        except KeyError:
            self.__logger.error(f"Unknown update frequency - {update_frequency}, available: {list(valid_frequencies.keys())}")

            return

        if not confirm_unstable_agreement and branch_name == "main" and update_frequency != "never":
            self.__logger.warning_unstable_branch(branch_name)

        if it_is_time_for_update:
            if not (Constants.GIT_PATH.exists() and Constants.GIT_PATH.is_dir()):
                self.__logger.error("Root directory of Allor is not a git repository. Update canceled.")

                return

            self.__update_allor(branch_name)

    def __get_timestamp(self):
        with open(Constants.TIMESTAMP_PATH, "r") as f:
            return json.load(f)

    def __create_timestamp(self):
        with open(Constants.TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": 0}, f, ensure_ascii=False, indent=4)

    def __update_timestamp(self):
        with open(Constants.TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": time.time()}, f, ensure_ascii=False, indent=4)

    def __update_allor(self, branch_name):
        try:
            import git

            from git import Repo
            from git import GitCommandError

            # noinspection PyTypeChecker, PyUnboundLocalVariable
            repo = Repo(Constants.ROOT_PATH, odbt=git.db.GitDB)
            current_commit = repo.head.commit.hexsha

            repo.remotes.origin.fetch()

            latest_commit = getattr(repo.remotes.origin.refs, branch_name).commit.hexsha

            if current_commit == latest_commit:
                if self.__config["updates"]["notify_if_no_new_updates"]:
                    self.__logger.info("No new updates.")
            else:
                if self.__config["updates"]["notify_if_has_new_updates"]:
                    self.__logger.info("New updates are available.")

                if self.__config["updates"]["auto_update"]:
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
                            self.__logger.error("An error occurred during the update. "
                                                "It is recommended to use \"hard\" update mode. "
                                                "But be careful, it erases all personal changes from Allor repository.")

                    elif update_mode == "hard":
                        repo.git.reset('--hard', 'origin/' + branch_name)
                    else:
                        self.__logger.error(f"Unknown update mode - {update_mode}, available: {valid_modes}")

                        return

                    self.__logger.info("Update complete.")

            self.__update_timestamp()

        except ImportError:
            self.__logger.error("GitPython is not installed.")
