import glob
import json
import os
import re
import sys
from datetime import datetime

from .Paths import Paths


class SingletonLogger(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonLogger, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonLogger):
    file = Paths.LOG_PATH

    def __init__(self):
        self.formatting = _Formatting()
        self.levels = {
            "FATAL": _Formatting.COLOR["RED"],
            "ERROR": _Formatting.COLOR["RED"],
            "WARN": _Formatting.COLOR["YELLOW"],
            "INFO": _Formatting.COLOR["BLUE"],
            "EMIT": _Formatting.COLOR["GREEN"],
            "DEBUG": _Formatting.COLOR["MAGENTA"],
            "TRACE": _Formatting.COLOR["CYAN"],
            "LINE": _Formatting.COLOR["DEFAULT"],
        }

        info = self.__get_info()

        if info["branch"] == "main":
            info["branch"] = "v.2"

        self.debug(f"{info['branch']} : {info['hex']}")

    def __log(self, text, level, display):
        if display:
            if level == "LINE":
                print()
            else:
                indent = " " * 9
                indented_text = "\n".join(line if i == 0 or not line else indent + line for i, line in enumerate(text.split("\n")))

                print(f"{self.formatting.foreground('[Allor]: ', self.levels.get(level), _Formatting.INTENSITY['BRIGHT'])}" + indented_text)

        if Logger.file:
            directory = Logger.file.parent

            if not directory.exists():
                directory.mkdir(parents=True)

            if not Logger.file.exists():
                log_files = list(glob.glob(str(directory / "log_*.log")))

                if len(log_files) > 5:
                    log_files.sort(key=os.path.getmtime)

                    os.remove(log_files[0])

                Logger.file.touch()

            with open(Logger.file, "a") as f:
                if level == "LINE":
                    f.write("\n")
                else:
                    indent = " " * 30
                    indented_text = "\n".join(line if i == 0 or not line else indent + line for i, line in enumerate(text.split("\n")))
                    indented_text = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub("", indented_text)

                    f.write(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}][{level:<5}]: {indented_text}\n")

    def fatal(self, text, display=True):
        self.__log(text, "FATAL", display)

    def error(self, text, display=True):
        self.__log(text, "ERROR", display)

    def warn(self, text, display=True):
        self.__log(text, "WARN", display)

    def info(self, text, display=True):
        self.__log(text, "INFO", display)

    def emit(self, text, display=True):
        self.__log(text, "EMIT", display)

    def debug(self, text, display=True):
        self.__log(text, "DEBUG", display)

    def trace(self, text, display=True):
        self.__log(text, "TRACE", display)

    def line(self, count=1, display=True):
        self.__log("\n" * count, "LINE", display)

    def warning_unstable_branch(self, branch_name="main"):
        def bold(text):
            return self.formatting.format(text, _Formatting.FORMAT["BOLD"])

        branch_name = bold(branch_name)
        allor_v2 = bold("Allor v.2")
        branch_name_param = bold("\"branch_name\"")
        v1 = bold("\"v.1\"")
        config_json = bold("config.json")
        confirm_unstable_param = bold("\"confirm_unstable\"")
        true = bold("\"true\"")

        warn_messages = (
            f"Attention! You are currently using an unstable {branch_name} update branch. \n"
            f"This branch is intended for the development of {allor_v2}. \n"
            f"Please be aware that changes made in {allor_v2} may disrupt your current workflow. \n"
            "Nodes may be renamed, parameters within them may be altered or even removed. \n"
            "If backward compatibility of your workflow is important to you, consider this. \n"
            f"You can change the {branch_name_param} parameter to {v1} in your {config_json}. \n"
            "If you are prepared for potential changes, you can modify your current workflow. \n"
            f"To accept, switch the {confirm_unstable_param} parameter in your {config_json} to {true}. \n"
            "This will result in this warning no longer appearing."
        )

        emit_messages = (
            "We appreciate your support and understanding during this transition period. \n"
            f"Thank you and welcome to {allor_v2}."
        )

        self.warn(warn_messages)
        self.line()
        self.emit(emit_messages)
        self.line()

    def __get_info(self):
        with open(Paths.INFO_PATH, "r") as f:
            return json.load(f)


class _Formatting:
    COLOR = {
        "BLACK": 0,
        "RED": 1,
        "GREEN": 2,
        "YELLOW": 3,
        "BLUE": 4,
        "MAGENTA": 5,
        "CYAN": 6,
        "WHITE": 7,
        "DEFAULT": 8,
        "GRAY_1": 232,
        "GRAY_2": 233,
        "GRAY_3": 234,
        "GRAY_4": 235,
        "GRAY_5": 236,
        "GRAY_6": 237,
        "GRAY_7": 238,
        "GRAY_8": 239,
        "GRAY_9": 240,
        "GRAY_10": 241,
        "GRAY_11": 242,
        "GRAY_12": 243,
        "GRAY_13": 244,
        "GRAY_14": 245,
        "GRAY_15": 246,
        "GRAY_16": 247,
        "GRAY_17": 248,
        "GRAY_18": 249,
        "GRAY_19": 250,
        "GRAY_20": 251,
        "GRAY_21": 252,
        "GRAY_22": 253,
        "GRAY_32": 254,
        "GRAY_24": 255
    }

    INTENSITY = {
        "NORMAL": 30,
        "BRIGHT": 90
    }

    FORMAT = {
        "BOLD": 1,
        "FAINT": 2,
        "ITALIC": 3,
        "UNDERLINE": 4,
        "BLINKING": 5,
        "FAST_BLINKING": 6,
        "REVERSE": 7,
        "HIDE": 8,
        "STRIKETHROUGH": 9,
    }

    def __init__(self):
        self.__ansi = self.__formatting_support()

    # noinspection PyPep8Naming
    def __formatting_support(self):
        platform = sys.platform

        if platform == "win32":
            import ctypes

            STD_OUTPUT_HANDLE = -11
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

            kernel32 = ctypes.WinDLL("kernel32")
            hStdOut = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            mode = ctypes.c_ulong()

            if not kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode)):
                return False

            if not mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING:
                return False

        if platform in ("linux", "darwin"):
            term = os.getenv("TERM")

            if term not in ("xterm", "xterm-256color", "vt100", "ansi", "linux"):
                return False

        return True

    def format(self, text, format_code):
        if self.__ansi:
            if re.search(r"\033\[\d+m", text):
                return re.sub(r"(\033\[\d+m)", r"\1;\033[" + str(format_code) + "m", text)
            else:
                return "\033[" + str(format_code) + "m" + text + "\033[0m"
        else:
            return text

    def foreground(self, text, color_code, intensity):
        if 232 <= color_code <= 255:
            intensity = 0

        if self.__ansi:
            if re.search(r"\033\[\d+m", text):
                return re.sub(r"(\033\[\d+m)", r"\1;\033[" + str(color_code + intensity) + "m", text)
            else:
                return "\033[" + str(color_code + intensity) + "m" + text + "\033[0m"
        else:
            return text

    def background(self, text, color_code, intensity):
        if 232 <= color_code <= 255:
            intensity = 0

        if self.__ansi:
            if re.search(r"\033\[\d+m", text):
                return re.sub(r"(\033\[\d+m)", r"\1;\033[" + str(color_code + 10 + intensity) + "m", text)
            else:
                return "\033[" + str(color_code + 10 + intensity) + "m" + text + "\033[0m"
        else:
            return text

    def reset(self, text):
        return re.compile(r'\033\[[0-?]*[ -/]*[@-~]').sub('', text)
