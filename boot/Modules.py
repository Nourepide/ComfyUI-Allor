import functools
from importlib import import_module

from .Backends import Backends


class Modules:
    def __init__(self, logger, config, backends):
        self.__logger = logger
        self.__config = config
        self.__backends = backends

    def initiate(self):
        modules_loaded = dict()
        modules_not_loaded = dict()

        modules_info = {
            "AlphaChanel": [Backends.TORCH],
            "Clamp": [],
            "ImageBatch": [Backends.TORCH],
            "ImageComposite": [Backends.TORCH, Backends.PIL],
            "ImageContainer": [Backends.TORCH],
            "ImageDraw": [Backends.PIL],
            "ImageEffects": [Backends.TORCH, Backends.NUMPY, Backends.CV2],
            "ImageFilter": [Backends.TORCH, Backends.PIL, Backends.CV2],
            "ImageNoise": [Backends.TORCH, Backends.NUMPY],
            "ImageSegmentation": [Backends.TORCH, Backends.PIL, Backends.REMBG],
            "ImageText": [Backends.PIL],
            "ImageTransform": [Backends.TORCH, Backends.PIL]
        }

        for module_name, backends in modules_info.items():
            if self.__config["modules"][module_name]:
                if self.__required(module_name, *backends):
                    if module := import_module(f"..modules.{module_name}", package=__package__):
                        modules_loaded.update(module.NODE_CLASS_MAPPINGS)
                else:
                    modules_not_loaded[module_name] = backends

        modules_len = len({k: v for k, v in self.__config["modules"].items() if v})
        nodes_len = len(modules_loaded)

        self.__logger.info(f"{modules_len} modules were enabled.", self.__config["logger"]["modules_enabled"])
        self.__logger.info(f"{nodes_len} nodes were loaded.", self.__config["logger"]["nodes_loaded"])

        return modules_loaded

    @functools.lru_cache
    def __required(self, module, *backends):
        for backend in backends:
            if not self.__backends[backend]:
                self.__logger.error(f"Module {module} did not find all necessary backends. Loading skipped.")
                return False
        return True
