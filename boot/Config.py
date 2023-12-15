import json

from .Paths import Paths


class Config:
    def __init__(self, logger):
        self.__logger = logger
        self.__template = self.__get_template()

        if not Paths.CONFIG_PATH.exists():
            self.__logger.info("Creating configuration file.")
            self.__create_config()

        self.__config = self.__get_config()

    def initiate(self):
        if not self.__verify_keys(self.__template, self.__config):
            self.__logger.info("Updating configuration file.")
            self.__update_config(self.__template, self.__config)

        return self.__get_config()

    def __create_config(self):
        with open(Paths.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.__template, f, ensure_ascii=False, indent=4)

    def __get_template(self):
        with open(Paths.TEMPLATE_PATH, "r") as f:
            template = json.load(f)

            if "__comment" in template:
                del template["__comment"]

            return template

    def __get_config(self):
        with open(Paths.CONFIG_PATH, "r") as f:
            return json.load(f)

    def __verify_keys(self, json1, json2):
        def get_keys(json_obj, prefix=''):
            keys = []

            for k, v in json_obj.items():
                if isinstance(v, dict):
                    keys.extend(get_keys(v, prefix + k + '.'))
                else:
                    keys.append(prefix + k)

            return set(keys)

        keys1 = get_keys(json1)
        keys2 = get_keys(json2)

        return keys1 == keys2

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

        with open(Paths.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(source, f, ensure_ascii=False, indent=4)
