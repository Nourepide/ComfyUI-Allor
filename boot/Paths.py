import os
import platform
from datetime import datetime
from pathlib import Path

import folder_paths


class Paths:
    ROOT_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    TEMPLATE_PATH = ROOT_PATH / "resources/template.json"
    TIMESTAMP_PATH = ROOT_PATH / "resources/timestamp.json"
    INFO_PATH = ROOT_PATH / "resources/info.json"
    CONFIG_PATH = ROOT_PATH / "config.json"
    GIT_PATH = ROOT_PATH / ".git"
    LOG_PATH = ROOT_PATH / f"resources/logs/log_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"

    def __init__(self, logger, config):
        self.__logger = logger
        self.__config = config

    def initiate(self):
        fonts_folder_path = self.__get_fonts_folder_path()

        os.environ["U2NET_HOME"] = folder_paths.models_dir + "/onnx"

        folder_paths.folder_names_and_paths["onnx"] = ([os.path.join(folder_paths.models_dir, "onnx")], {".onnx"})
        folder_paths.folder_names_and_paths["fonts"] = (fonts_folder_path, {".otf", ".ttf"})

    def __get_fonts_folder_path(self):
        system = platform.system()
        user_home = os.path.expanduser('~')

        config_font_path = os.path.join(folder_paths.base_path, *self.__config["fonts"]["folder_path"].replace("\\", "/").split("/"))

        if not os.path.exists(config_font_path):
            os.makedirs(config_font_path, exist_ok=True)

        paths = [config_font_path]

        if self.__config["fonts"]["system_fonts"]:
            if system == "Windows":
                paths.append(os.path.join(os.environ["WINDIR"], "Fonts"))
            elif system == "Darwin":
                paths.append(os.path.join("/Library", "Fonts"))
            elif system == "Linux":
                paths.append(os.path.join("/usr", "share", "fonts"))
                paths.append(os.path.join("/usr", "local", "share", "fonts"))

        if self.__config["fonts"]["user_fonts"]:
            if system == "Darwin":
                paths.append(os.path.join(user_home, "Library", "Fonts"))
            elif system == "Linux":
                paths.append(os.path.join(user_home, ".fonts"))

        return [path for path in paths if os.path.exists(path)]
