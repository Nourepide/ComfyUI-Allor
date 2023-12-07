import nodes
from .Logger import Logger


class Override:
    def __init__(self, config):
        self.__logger = Logger()
        self.__config = config

    def initiate(self):
        override_nodes_len = 0

        def override(function):
            start_len = nodes.NODE_CLASS_MAPPINGS.__len__()

            nodes.NODE_CLASS_MAPPINGS = dict(
                filter(function, nodes.NODE_CLASS_MAPPINGS.items())
            )

            return start_len - nodes.NODE_CLASS_MAPPINGS.__len__()

        if self.__config["override"]["postprocessing"]:
            override_nodes_len += override(lambda item: not item[1].CATEGORY.startswith("image/postprocessing"))

        if self.__config["override"]["transform"]:
            override_nodes_len += override(lambda item: not item[0] == "ImageScale" and not item[0] == "ImageScaleBy" and not item[0] == "ImageInvert")

        if self.__config["override"]["debug"]:
            nodes.VAEDecodeTiled.CATEGORY = "latent"
            nodes.VAEEncodeTiled.CATEGORY = "latent"

            override_nodes_len += override(lambda item: not item[1].CATEGORY.startswith("_for_testing"))

        self.__logger.info(str(override_nodes_len) + " nodes were overridden.")
