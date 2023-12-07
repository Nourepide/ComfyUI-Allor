import glob
import os
import re

from .Constants import Constants


class Logger:
    file = Constants.LOG_PATH
    levels = {
        "FATAL": 92,
        "ERROR": 91,
        "WARN": 93,
        "INFO": 94,
        "DEBUG": 95,
        "TRACE": 96,
        "LINE": 0
    }

    def __init__(self):
        pass

    def __log(self, text, level):
        if level == "LINE":
            print()
        else:
            print(f"\033[{self.levels.get(level, '')}m[Allor]\033[0m: " + text)

        if Logger.file:
            directory = Logger.file.parent

            if not directory.exists():
                directory.mkdir(parents=True)

            if not Logger.file.exists():
                log_files = list(glob.glob(str(directory / 'log_*.txt')))

                if len(log_files) > 5:
                    log_files.sort(key=os.path.getmtime)

                    os.remove(log_files[0])

                Logger.file.touch()

            with open(Logger.file, "a") as f:
                if level == "LINE":
                    f.write("\n")
                else:
                    text = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub("", text)

                    f.write(f"[{level}]: {text}\n")

    def fatal(self, text):
        self.__log(text, "FATAL")

    def error(self, text):
        self.__log(text, "ERROR")

    def warn(self, text):
        self.__log(text, "WARN")

    def info(self, text):
        self.__log(text, "INFO")

    def debug(self, text):
        self.__log(text, "DEBUG")

    def trace(self, text):
        self.__log(text, "TRACE")

    def line(self, count=1):
        self.__log("\n" * count, "LINE")

    def warning_unstable_branch(self, branch_name="main"):
        warn_messages = [
            f"Attention! You are currently using an unstable \033[1m{branch_name}\033[0m update branch.",
            f"This branch is intended for the development of \033[1mAllor v.2\033[0m.",
            f"Please be aware that changes made in \033[1mAllor v.2\033[0m may disrupt your current workflow.",
            "Nodes may be renamed, parameters within them may be altered or even removed.",
            "If backward compatibility of your workflow is important to you, consider this.",
            f"You can change the \033[1m\"branch_name\"\033[0m parameter to \033[1m\"v.1\"\033[0m in your \033[1mconfig.json.\033[0m",
            "If you are prepared for potential changes, you can modify your current workflow.",
            f"To accept, switch the \033[1m\"confirm_unstable\"\033[0m parameter in your \033[1mconfig.json.\033[0m to \033[1m\"true\".\033[0m",
            "This will result in this warning no longer appearing."
        ]

        info_messages = [
            "We appreciate your support and understanding during this transition period.",
            f"Thank you and welcome to \033[1mAllor v.2\033[0m.\n"
        ]

        for message in warn_messages:
            self.warn(message)

        self.line()

        for message in info_messages:
            self.info(message)
