import json
import os

import folder_paths
import nodes


class Loader:
    def __init__(self):
        pass

    def __log(self, text):
        print("\033[92m[Allor]\033[0m: " + text)

    def __get_config(self):
        root = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(root, "config.json"), "r") as f:
            return json.load(f)

    config = __get_config

    def __get_fonts_folder_path(self):
        return os.path.join(folder_paths.base_path, *self.config()["fonts_folder_path"])

    def setup_rembg(self):
        os.environ["U2NET_HOME"] = folder_paths.models_dir + "/onnx"

    def setup_paths(self):
        fonts_folder_path = self.__get_fonts_folder_path()

        folder_paths.folder_names_and_paths["onnx"] = ([os.path.join(folder_paths.models_dir, "onnx")], {".onnx"})
        folder_paths.folder_names_and_paths["fonts"] = ([fonts_folder_path], {".otf", ".ttf"})

        if not os.path.exists(fonts_folder_path):
            os.mkdir(fonts_folder_path)

    def setup_override(self):
        override_nodes_len = 0

        def override(function):
            start_len = nodes.NODE_CLASS_MAPPINGS.__len__()

            nodes.NODE_CLASS_MAPPINGS = dict(
                filter(function, nodes.NODE_CLASS_MAPPINGS.items())
            )

            return start_len - nodes.NODE_CLASS_MAPPINGS.__len__()

        if self.config()["override"]["postprocessing"]:
            override_nodes_len += override(lambda item: not item[1].CATEGORY.startswith("image/postprocessing"))

        if self.config()["override"]["transform"]:
            override_nodes_len += override(lambda item: not item[0] == "ImageScale" and not item[0] == "ImageInvert")

        self.__log(str(override_nodes_len) + " standard nodes was overridden.")

    def get_modules(self):
        modules = dict()

        if self.config()["modules"]["AlphaChanel"]:
            from .modules import AlphaChanel
            modules.update(AlphaChanel.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["Clamp"]:
            from .modules import Clamp
            modules.update(Clamp.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageComposite"]:
            from .modules import ImageComposite
            modules.update(ImageComposite.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageContainer"]:
            from .modules import ImageContainer
            modules.update(ImageContainer.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageDraw"]:
            from .modules import ImageDraw
            modules.update(ImageDraw.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageFilter"]:
            from .modules import ImageFilter
            modules.update(ImageFilter.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageSegmentation"]:
            from .modules import ImageSegmentation
            modules.update(ImageSegmentation.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageText"]:
            from .modules import ImageText
            modules.update(ImageText.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageTransform"]:
            from .modules import ImageTransform
            modules.update(ImageTransform.NODE_CLASS_MAPPINGS)

        modules_len = dict(
            filter(
                lambda item: item[1],
                self.config()["modules"].items()
            )
        ).__len__()

        nodes_len = modules.__len__()

        self.__log(str(modules_len) + " modules enabled.")
        self.__log(str(nodes_len) + " nodes was loaded.")

        return modules
