import os
import platform
from datetime import datetime
from importlib import import_module
from pathlib import Path

from .Backends import Backends


class Paths:
    ROOT_PATH = Path(__file__).resolve().parent.parent
    RESOURCE_PATH = ROOT_PATH / "resources"
    TEMPLATE_PATH = RESOURCE_PATH / "template.json"
    TIMESTAMP_PATH = RESOURCE_PATH / "timestamp.json"
    INFO_PATH = RESOURCE_PATH / "info.json"
    LOG_PATH = RESOURCE_PATH / f"logs/log_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
    CONFIG_PATH = ROOT_PATH / "config.json"
    GIT_PATH = ROOT_PATH / ".git"

    def __init__(self, logger, config, backends):
        self.__logger = logger
        self.__config = config
        self.__backends = backends

    def initiate(self):
        if self.__backends[Backends.COMFY_UI]:
            folder_paths = import_module("folder_paths")
            fonts_folder_path = self.__get_font_paths(folder_paths)

            os.environ["U2NET_HOME"] = str(Path(folder_paths.models_dir) / "onnx")

            folder_paths.folder_names_and_paths.update({
                "onnx": ([Path(folder_paths.models_dir) / "onnx"], {".onnx"}),
                "fonts": (fonts_folder_path, {".otf", ".ttf"})
            })

    def __get_font_paths(self, folder_paths):
        system = platform.system()
        user_home = Path.home()

        config_font_path = Path(folder_paths.base_path) / Path(self.__config["fonts"]["folder_path"].replace("\\", "/"))
        config_font_path.mkdir(parents=True, exist_ok=True)

        system_fonts_paths = {
            "Windows": [Path(os.environ.get("WINDIR", "")) / "Fonts"],
            "Darwin": [Path("/Library") / "Fonts", user_home / "Library" / "Fonts"],
            "Linux": [Path("/usr") / "share" / "fonts", Path("/usr") / "local" / "share" / "fonts", user_home / ".fonts"]
        }

        paths = [config_font_path] + system_fonts_paths.get(system, [])

        return [str(path) for path in paths if path.exists()]
