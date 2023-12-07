from .Logger import Logger


class Modules:
    def __init__(self, config):
        self.__logger = Logger()
        self.__config = config

    def initiate(self):
        modules = dict()

        if self.__config["modules"]["AlphaChanel"]:
            from ..modules import AlphaChanel
            modules.update(AlphaChanel.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["Clamp"]:
            from ..modules import Clamp
            modules.update(Clamp.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageBatch"]:
            from ..modules import ImageBatch
            modules.update(ImageBatch.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageComposite"]:
            from ..modules import ImageComposite
            modules.update(ImageComposite.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageContainer"]:
            from ..modules import ImageContainer
            modules.update(ImageContainer.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageDraw"]:
            from ..modules import ImageDraw
            modules.update(ImageDraw.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageEffects"]:
            from ..modules import ImageEffects
            modules.update(ImageEffects.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageFilter"]:
            from ..modules import ImageFilter
            modules.update(ImageFilter.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageNoise"]:
            from ..modules import ImageNoise
            modules.update(ImageNoise.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageSegmentation"]:
            from ..modules import ImageSegmentation
            modules.update(ImageSegmentation.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageText"]:
            from ..modules import ImageText
            modules.update(ImageText.NODE_CLASS_MAPPINGS)

        if self.__config["modules"]["ImageTransform"]:
            from ..modules import ImageTransform
            modules.update(ImageTransform.NODE_CLASS_MAPPINGS)

        modules_len = dict(
            filter(
                lambda item: item[1],
                self.__config["modules"].items()
            )
        ).__len__()

        nodes_len = modules.__len__()

        self.__logger.info(str(modules_len) + " modules were enabled.")
        self.__logger.info(str(nodes_len) + " nodes were loaded.")

        return modules
