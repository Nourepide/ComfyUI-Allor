import json
import os

import folder_paths
import nodes


class Loader:
    def __init__(self):
        pass

    __root_path = os.path.dirname(os.path.abspath(__file__))
    __template_path = os.path.join(__root_path, "template/template.json")
    __config_path = os.path.join(__root_path, "config.json")

    def __log(self, text):
        print("\033[92m[Allor]\033[0m: " + text)

    def __error(self, text):
        print("\033[91m[Allor]\033[0m: " + text)

    def __notification(self, text):
        print("\033[94m[Allor]\033[0m: " + text)

    def __get_template(self):
        with open(self.__template_path, "r") as f:
            template = json.load(f)

            if "__comment" in template:
                del template["__comment"]

            return template

    def __create_config(self):
        with open(self.__config_path, "w", encoding="utf-8") as f:
            json.dump(self.__template(), f, ensure_ascii=False, indent=4)

    def __get_config(self):
        with open(self.__config_path, "r") as f:
            return json.load(f)

    def __update_config(self, template, source):
        for k, v in template.items():
            if k not in source:
                if isinstance(v, dict):
                    source[k] = {}
                else:
                    source[k] = v

            if isinstance(v, dict):
                self.__update_config(v, source[k])

        keys_to_delete = [k for k in source if k not in template]

        for k in keys_to_delete:
            del source[k]

        with open(self.__config_path, "w", encoding="utf-8") as f:
            json.dump(source, f, ensure_ascii=False, indent=4)

    __template = __get_template
    __config = __get_config

    def __get_fonts_folder_path(self):
        return os.path.join(folder_paths.base_path, *self.__config()["fonts_folder_path"])

    def __get_keys(self, json_obj, prefix=''):
        keys = []

        for k, v in json_obj.items():
            if isinstance(v, dict):
                keys.extend(self.__get_keys(v, prefix + k + '.'))
            else:
                keys.append(prefix + k)

        return set(keys)

    def __check_json_keys(self, json1, json2):
        keys1 = self.__get_keys(json1)
        keys2 = self.__get_keys(json2)

        return keys1 == keys2

    def setup_config(self):
        if not os.path.exists(self.__config_path):
            self.__log("Creating config.json")
            self.__create_config()
        else:
            if not self.__check_json_keys(self.__template(), self.__config()):
                self.__log("Updating config.json")
                self.__update_config(self.__template(), self.__config())

    def check_updates(self):
        if self.__config()["updates"]["check_updates"]:
            try:
                import git
                from git import Repo

                # noinspection PyTypeChecker, PyUnboundLocalVariable
                repo = Repo(self.__root_path, odbt=git.db.GitDB)
                current_commit = repo.head.commit.hexsha

                repo.remotes.origin.fetch()

                # noinspection PyUnresolvedReferences
                branch_name = self.__config()["updates"]["branch_name"]
                latest_commit = getattr(repo.remotes.origin.refs, branch_name).commit.hexsha

                if current_commit == latest_commit:
                    if self.__config()["updates"]["notify_if_no_new_updates"]:
                        self.__notification("No new updates.")
                else:
                    if self.__config()["updates"]["notify_if_has_new_updates"]:
                        self.__notification("New updates are available.")

                    if self.__config()["updates"]["auto_update"]:
                        repo.remotes.origin.pull()
                        self.__notification("Update complete.")
            except ImportError:
                self.__error("GitPython is not installed.")
                return

        

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

        if self.__config()["override"]["postprocessing"]:
            override_nodes_len += override(lambda item: not item[1].CATEGORY.startswith("image/postprocessing"))

        if self.__config()["override"]["transform"]:
            override_nodes_len += override(lambda item: not item[0] == "ImageScale" and not item[0] == "ImageScaleBy" and not item[0] == "ImageInvert")

        if self.__config()["override"]["debug"]:
            nodes.VAEDecodeTiled.CATEGORY = "latent"
            nodes.VAEEncodeTiled.CATEGORY = "latent"

            override_nodes_len += override(lambda item: not item[1].CATEGORY.startswith("_for_testing"))

        self.__log(str(override_nodes_len) + " standard nodes was overridden.")

    def get_modules(self):
        modules = dict()

        if self.__config()["modules"]["AlphaChanel"]:
            from .modules import AlphaChanel
            modules.update(AlphaChanel.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["Clamp"]:
            from .modules import Clamp
            modules.update(Clamp.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageBatch"]:
            from .modules import ImageBatch
            modules.update(ImageBatch.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageComposite"]:
            from .modules import ImageComposite
            modules.update(ImageComposite.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageContainer"]:
            from .modules import ImageContainer
            modules.update(ImageContainer.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageDraw"]:
            from .modules import ImageDraw
            modules.update(ImageDraw.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageEffects"]:
            from .modules import ImageEffects
            modules.update(ImageEffects.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageFilter"]:
            from .modules import ImageFilter
            modules.update(ImageFilter.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageNoise"]:
            from .modules import ImageNoise
            modules.update(ImageNoise.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageSegmentation"]:
            from .modules import ImageSegmentation
            modules.update(ImageSegmentation.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageText"]:
            from .modules import ImageText
            modules.update(ImageText.NODE_CLASS_MAPPINGS)

        if self.__config()["modules"]["ImageTransform"]:
            from .modules import ImageTransform
            modules.update(ImageTransform.NODE_CLASS_MAPPINGS)

        modules_len = dict(
            filter(
                lambda item: item[1],
                self.__config()["modules"].items()
            )
        ).__len__()

        nodes_len = modules.__len__()

        self.__log(str(modules_len) + " modules enabled.")
        self.__log(str(nodes_len) + " nodes was loaded.")

        return modules
