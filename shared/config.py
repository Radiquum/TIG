import yaml
import os
from .util import check_int, check_hex
from .log import log
import json
from sys import exit


class Config:

    def check_path(self, path: str = "config.yaml"):
        lower_path = path.lower()
        if not lower_path.endswith(".yaml") and not lower_path.endswith(".json"):
            log.error(
                "Invalid config file extension provided, should be .yaml or .json"
            )
            exit(1)
        if os.path.exists(path):
            log.info(f"using config file `{path}`")
            return True
        else:
            log.info(f"created new config file `{path}`")
            self.save(path)

    def __init__(self):
        self.config_file = "config.yaml"
        self._conf = {
            "resolution": {
                "width": 1920,
                "height": 1080,
            },
            "font": {"file": "./fonts/BebasNeue/Bebas_Neue_Regular.ttf", "size": 72},
            "text": {"color": "#ffffff"},
            "background": {"color": "#000000"},
        }

    def get_keys(self):
        return list(self._conf.keys())

    def get_section(self, section: str):
        return self._conf[section]

    def get_section_keys(self, section: str):
        return list(self._conf[section].keys())

    def get_section_key(self, section: str, key: str):
        return self._conf[section][key]

    def get_config_section_key_type(self, section: str, key: str):
        ktype = self.get_section_key(section, key)
        if isinstance(ktype, int):
            return "number"
        if key == "color":
                return "hex[value] | rgb[0-255,0-255,0-255]"
        if isinstance(ktype, str):
                return "string"

    def get_config_sections_and_keys(self):
        string = ""
        for sect in self.get_keys():
            string += f"{sect}:\n"
            for key in self.get_section_keys(sect):
                string += f"  - {key}\n"
        return string

    def get_config_sections_and_keys_types(self):
        string = ""
        for sect in self.get_keys():
            string += f"{sect}:\n"
            for key in self.get_section_keys(sect):
                string += f"  - {key}: {self.get_config_section_key_type(sect, key)}\n"

        return string

    def save(self, path: str | None = None):
        if path is None:
            path = self.config_file
        lower_path = path.lower()

        if lower_path.endswith(".json"):
            with open(path, "w") as fp:
                json.dump(self.dict(), fp, indent=2)
        elif lower_path.endswith(".yaml"):
            _yaml = yaml.dump(self._conf)
            with open(path, "w") as fp:
                fp.write(_yaml)
        else:
            log.error(
                "Invalid config file extension provided, should be .yaml or .json"
            )
            exit(1)

    def load(self, path: str | None = None):
        if path is None:
            path = self.config_file
        self.check_path(path)
        lower_path = path.lower()

        if lower_path.endswith(".json"):
            with open(path, "r") as fp:
                conf: dict = json.load(fp)
        elif lower_path.endswith(".yaml"):
            with open(path, "r") as fp:
                conf: dict = yaml.load(fp, yaml.Loader)
        else:
            log.error(
                "Invalid config file extension provided, should be .yaml or .json"
            )
            exit(1)

        self.config_file = path
        self._conf = conf

    def dict(self):
        return self._conf

    def json(self):
        return json.dumps(self.dict(), indent=2)

    def yaml(self):
        return yaml.dump(self.dict())

    def update(self, section, key, value):
        self._conf[section][key] = value

    def update_and_save(self, section, key, value):
        self.update(section, key, value)
        self.save()


config = Config()
