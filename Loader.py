import json
import os
import platform
import time

from pathlib import Path

import folder_paths
import nodes


class Loader:
    def __init__(self):
        pass

    __ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    __TEMPLATE_PATH = os.path.join(__ROOT_PATH, "template/template.json")
    __TIMESTAMP_PATH = os.path.join(__ROOT_PATH, "template/timestamp.json")
    __CONFIG_PATH = os.path.join(__ROOT_PATH, "config.json")

    __DAY_SECONDS = 24 * 60 * 60
    __WEEK_SECONDS = 7 * __DAY_SECONDS
    __MONTH_SECONDS = 30 * __DAY_SECONDS

    def __log(self, text):
        print("\033[92m[Allor]\033[0m: " + text)

    def __error(self, text):
        print("\033[91m[Allor]\033[0m: " + text)

    def __notification(self, text):
        print("\033[94m[Allor]\033[0m: " + text)

    def __new_line(self):
        print()

    def __warning_unstable_branch(self):
        self.__new_line()
        self.__error("Attention! You are currently using an unstable \"main\" update branch intended for the development of Allor 2.")
        self.__error("Please be aware that changes made in Allor 2 may disrupt your current workflow.")
        self.__error("Nodes may be renamed, parameters within them may be altered or even removed.")
        self.__new_line()
        self.__error("If backward compatibility of your workflow is important to you, "
                     "you can change the \"branch_name\" parameter to \"allor-1\" in your config.json.")
        self.__error("Switch the \"confirm_unstable_agreement\" parameter in your config.json to \"true\", "
                     "if you are prepared for potential changes and are willing to modify your current workflow from time to time.")
        self.__error("This will result in this warning no longer appearing.")
        self.__new_line()
        self.__notification("We appreciate your support and understanding during this transition period.")
        self.__notification("Thank you for using Allor 2.\n")

    def __create_config(self):
        with open(self.__CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.__template(), f, ensure_ascii=False, indent=4)

    def __create_timestamp(self):
        with open(self.__TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": 0}, f, ensure_ascii=False, indent=4)

    def __get_template(self):
        with open(self.__TEMPLATE_PATH, "r") as f:
            template = json.load(f)

            if "__comment" in template:
                del template["__comment"]

            return template

    def __get_config(self):
        with open(self.__CONFIG_PATH, "r") as f:
            return json.load(f)

    def __get_timestamp(self):
        with open(self.__TIMESTAMP_PATH, "r") as f:
            return json.load(f)

    def __update_config(self, template, source):
        def update_source(__template, __source):
            for k, v in __template.items():
                if k not in __source:
                    if isinstance(v, dict):
                        __source[k] = {}
                    else:
                        __source[k] = v

                if isinstance(v, dict):
                    __source[k] = update_source(v, __source[k])

            return __source

        def delete_keys(__template, __source):
            keys_to_delete = [k for k in __source if k not in __template]

            for k in keys_to_delete:
                del __source[k]

            return __source

        def sync_order(__template, __source):
            new_source = {}

            for key in __template:
                if key in __source:
                    if isinstance(__template[key], dict):
                        new_source[key] = sync_order(__template[key], __source[key])
                    else:
                        new_source[key] = __source[key]

            return new_source

        source = update_source(template, source)
        source = delete_keys(template, source)
        source = sync_order(template, source)

        with open(self.__CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(source, f, ensure_ascii=False, indent=4)

    def __update_timestamp(self):
        with open(self.__TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": time.time()}, f, ensure_ascii=False, indent=4)

    __template = __get_template
    __config = __get_config
    __timestamp = __get_timestamp

    def __get_fonts_folder_path(self):
        system = platform.system()
        user_home = os.path.expanduser('~')

        config_font_path = os.path.join(folder_paths.base_path, *self.__config()["fonts"]["folder_path"].replace("\\", "/").split("/"))

        if not os.path.exists(config_font_path):
            os.makedirs(config_font_path, exist_ok=True)

        paths = [config_font_path]

        if self.__config()["fonts"]["system_fonts"]:
            if system == "Windows":
                paths.append(os.path.join(os.environ["WINDIR"], "Fonts"))
            elif system == "Darwin":
                paths.append(os.path.join("/Library", "Fonts"))
            elif system == "Linux":
                paths.append(os.path.join("/usr", "share", "fonts"))
                paths.append(os.path.join("/usr", "local", "share", "fonts"))

        if self.__config()["fonts"]["user_fonts"]:
            if system == "Darwin":
                paths.append(os.path.join(user_home, "Library", "Fonts"))
            elif system == "Linux":
                paths.append(os.path.join(user_home, ".fonts"))

        return [path for path in paths if os.path.exists(path)]

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
        if not os.path.exists(self.__CONFIG_PATH):
            self.__log("Creating config.json")
            self.__create_config()
        else:
            if not self.__check_json_keys(self.__template(), self.__config()):
                self.__log("Updating config.json")
                self.__update_config(self.__template(), self.__config())

    def setup_timestamp(self):
        if not os.path.exists(self.__TIMESTAMP_PATH):
            self.__log("Creating timestamp.json")
            self.__create_timestamp()

    def check_updates(self):
        # confirm_unstable_agreement = self.__config()["updates"]["confirm_unstable_agreement"]
        confirm_unstable_agreement = True
        branch_name = self.__config()["updates"]["branch_name"]
        update_frequency = self.__config()["updates"]["update_frequency"].lower()
        valid_frequencies = ["always", "day", "week", "month", "never"]
        time_difference = time.time() - self.__timestamp()["timestamp"]

        if update_frequency == valid_frequencies[0]:
            it_is_time_for_update = True
        elif update_frequency == valid_frequencies[1]:
            it_is_time_for_update = time_difference >= self.__DAY_SECONDS
        elif update_frequency == valid_frequencies[2]:
            it_is_time_for_update = time_difference >= self.__WEEK_SECONDS
        elif update_frequency == valid_frequencies[3]:
            it_is_time_for_update = time_difference >= self.__MONTH_SECONDS
        elif update_frequency == valid_frequencies[4]:
            it_is_time_for_update = False
        else:
            self.__error(f"Unknown update frequency - {update_frequency}, available: {valid_frequencies}")

            return

        if not confirm_unstable_agreement and branch_name == "main" and update_frequency != "never":
            self.__warning_unstable_branch()

        if it_is_time_for_update:
            if not (Path(".git").exists() or Path(".git").is_dir()):
                self.__error("Root directory of Allor is not a git repository. Update canceled.")

                return

            try:
                import git

                from git import Repo
                from git import GitCommandError

                # noinspection PyTypeChecker, PyUnboundLocalVariable
                repo = Repo(self.__ROOT_PATH, odbt=git.db.GitDB)
                current_commit = repo.head.commit.hexsha

                repo.remotes.origin.fetch()

                latest_commit = getattr(repo.remotes.origin.refs, branch_name).commit.hexsha

                if current_commit == latest_commit:
                    if self.__config()["updates"]["notify_if_no_new_updates"]:
                        self.__notification("No new updates.")
                else:
                    if self.__config()["updates"]["notify_if_has_new_updates"]:
                        self.__notification("New updates are available.")

                    if self.__config()["updates"]["auto_update"]:
                        update_mode = self.__config()["updates"]["update_mode"].lower()
                        valid_modes = ["soft", "hard"]

                        if repo.active_branch.name != branch_name:
                            try:
                                repo.git.checkout(branch_name)
                            except GitCommandError:
                                self.__error(f"An error occurred while switching to the branch {branch_name}.")

                                return

                        if update_mode == "soft":
                            try:
                                repo.git.pull()
                            except GitCommandError:
                                self.__error("An error occurred during the update. "
                                             "It is recommended to use \"hard\" update mode. "
                                             "But be careful, it erases all personal changes from Allor repository.")

                        elif update_mode == "hard":
                            repo.git.reset('--hard', 'origin/' + branch_name)
                        else:
                            self.__error(f"Unknown update mode - {update_mode}, available: {valid_modes}")

                            return

                        self.__notification("Update complete.")

                self.__update_timestamp()

            except ImportError:
                self.__error("GitPython is not installed.")

    def setup_rembg(self):
        os.environ["U2NET_HOME"] = folder_paths.models_dir + "/onnx"

    def setup_paths(self):
        fonts_folder_path = self.__get_fonts_folder_path()

        folder_paths.folder_names_and_paths["onnx"] = ([os.path.join(folder_paths.models_dir, "onnx")], {".onnx"})
        folder_paths.folder_names_and_paths["fonts"] = (fonts_folder_path, {".otf", ".ttf"})

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
