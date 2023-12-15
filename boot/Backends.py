from importlib import import_module


class Backends:
    COMFY_UI = "main"
    TORCH = "torch"
    NUMPY = "numpy"
    CV2 = "cv2"
    PIL = "PIL"
    REMBG = "rembg"
    GIT = "git"

    def __init__(self, logger):
        self.__logger = logger
        self.__backends = [Backends.COMFY_UI, Backends.TORCH, Backends.NUMPY, Backends.CV2, Backends.PIL, Backends.REMBG, Backends.GIT]

    def initiate(self):
        dependencies = {}

        for backend in self.__backends:
            try:
                import_module(backend)
                dependencies[backend] = True
            except ImportError:
                self.__logger.error(f"Loading {backend} library ended with an error.")
                dependencies[backend] = False

        return dependencies
