import json
import os

import folder_paths
from .modules import AlphaChanel, Clamp, ImageComposite, ImageContainer, ImageSegmentation, ImageText


class Loader:
    def __init__(self):
        pass

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

    def get_modules(self):
        modules = dict()

        if self.config()["modules"]["AlphaChanel"]:
            modules.update(AlphaChanel.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["Clamp"]:
            modules.update(Clamp.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageComposite"]:
            modules.update(ImageComposite.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageContainer"]:
            modules.update(ImageContainer.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageSegmentation"]:
            modules.update(ImageSegmentation.NODE_CLASS_MAPPINGS)

        if self.config()["modules"]["ImageText"]:
            modules.update(ImageText.NODE_CLASS_MAPPINGS)

        return modules
