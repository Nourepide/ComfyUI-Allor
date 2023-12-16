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
            "FATAL": "r",
            "ERROR": "r",
            "WARN": "y",
            "INFO": "b",
            "EMIT": "g",
            "DEBUG": "m",
            "TRACE": "c",
            "LINE": "n"
        }

        self.__length = max(len(key) for key in self.levels)

        info = self.__get_info()

        if info["branch"] == "main":
            info["branch"] = "v.2"

        self.debug(f"{info['branch']} : {info['hex']}")

    def __log(self, text, level, display):
        text = self.formatting.format(text)

        if display:
            if level == "LINE":
                print()
            else:
                prefix = self.formatting.format(f"!![f{self.levels.get(level)}b;" + re.escape("[Allor]") + ":" + "] ")
                postfix = self.formatting.format(text, 9)

                print(f"{prefix}{postfix}")

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
                    prefix = f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}][{level:<{self.__length}}]: "
                    postfix = self.formatting.format(text, len(prefix))
                    postfix = self.formatting.reset(postfix)

                    f.write(f"{prefix}{postfix}\n")

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
        warn_messages = (
            f"Attention! You are currently using an unstable !![fyb;{branch_name}] update branch. \n"
            f"This branch is intended for the development of !![fmb;Allor v.2]. \n\n"
            f"Please be aware that changes made in !![fmb;Allor v.2] may disrupt your current workflow. \n"
            "Nodes may be renamed, parameters within them may be altered or even removed. \n\n"
            "If backward compatibility of your workflow is important to you, consider this. \n"
            f"You can change the !![fcb;branch_name_param] parameter to !![fbb;v1] in your !![fgb;config_json]. \n\n"
            "If you are prepared for potential changes, you can modify your configuration file. \n"
            f"To accept, switch the !![fcb;confirm_unstable_param] parameter in your !![fgb;config_json] to !![fbb;true]. \n"
            "This will result in this warning no longer appearing."
        )

        emit_messages = (
            "We appreciate your support and understanding during this transition period. \n"
            f"Thank you and welcome to !![fmb;Allor v.2]."
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
        "d": 0,  # DARK
        "r": 1,  # RED
        "g": 2,  # GREEN
        "y": 3,  # YELLOW
        "b": 4,  # BLUE
        "m": 5,  # MAGENTA
        "c": 6,  # CYAN
        "w": 7,  # WHITE
        "n": 8   # NORMAL
    }

    INTENSITY = {
        "n": 30,  # NORMAL
        "b": 90   # BRIGHT
    }

    ATTRIBUTE = {
        "n": 0,  # NORMAL
        "b": 1,  # BOLD
        "f": 2,  # FAINT
        "i": 3,  # ITALIC
        "u": 4,  # UNDERLINE
        "l": 5,  # BLINKING
        "a": 6,  # FAST_BLINKING
        "r": 7,  # REVERSE
        "h": 8,  # HIDE
        "s": 9   # STRIKETHROUGH
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

    def format(self, text, intend=0):
        if self.__ansi:
            text = self.__interpolation(text)
        else:
            text = self.__extraction(text)

        if intend > 0:
            text = "\n".join(line if i == 0 or not line else " " * intend + line for i, line in enumerate(text.split("\n")))

        return text

    def reset(self, text):
        return re.compile(r"\033\[[0-?]*[ -/]*[@-~]").sub("", text)

    def __interpolation(self, input_string):
        pattern = re.compile(r"!!\[(.*?)(?<!\\)]")

        def replace_func(match):
            params = match.group(1).split(';')

            fg, bg, attr, text = "fnn", "bnn", "an", None

            for param in params:
                if (len(param) == 3
                        and param[0] in ["f", "b"]
                        and param[1] in self.COLOR
                        and param[2] in self.INTENSITY):

                    if param[0] == "f":
                        fg = param
                    else:
                        bg = param
                elif len(param) == 2 and param[0] == "a" and param[1] in self.ATTRIBUTE:
                    attr = param
                else:
                    text = param

            text = text.replace("\\", "")

            return (f"\033["
                    f"{self.COLOR[fg[1]] + self.INTENSITY[fg[2]]};"
                    f"{self.COLOR[bg[1]] + self.INTENSITY[bg[2]] + 10};"
                    f"{self.ATTRIBUTE[attr[1]]}m{text}\033[0m")

        return pattern.sub(replace_func, input_string)

    def __extraction(self, input_string):
        pattern = re.compile(r"!!\[(.*?)(?<!\\)]")

        def replace_func(match):
            return match.group(1).split(":")[-1]

        return pattern.sub(replace_func, input_string)
