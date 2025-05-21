import yaml
import os
from rich import print
from .util import check_int, check_hex


class Config:

    def check_path(self, path: str = "config.yaml"):
        if os.path.exists(path):
            return True
        print(f"[bold red]ERROR:[/bold red] Config file `{path}` not found.")
        os._exit(1)

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

    def check_value_type(
        self, section: str, key: str, value: str | int
    ) -> tuple[bool, str]:
        if section in ["resolution"] and key in self.get_section_keys("resolution"):
            if check_int(value):
                return True, "number"
            return False, "number"
        if section in ["font"]:
            if key == "size":
                if check_int(value):
                    return True, "number"
                return False, "number"
            return True, "string"
        if section in ["text", "background"] and key in self.get_section_keys("text"):
            return check_hex(value), "xxxxxx"
        raise

    def save(self, path: str | None = None):
        if path is None:
            path = self.config_file

        _yaml = yaml.dump(self._conf)
        with open(path, "w") as fp:
            fp.write(
                f"# CREATED BY TIG\n# DO NOT EDIT DIRECTLY UNLESS YOU KNOW WHAT YOU ARE DOING, OTHERWISE USE config set COMMAND!\n\n{_yaml}"
            )

    def load(self, path: str | None = None):
        if path is None:
            path = self.config_file
        self.check_path(path)

        with open(path, "r") as fp:
            conf: dict = yaml.load(fp, yaml.Loader)
            self.config_file = path
            self._conf["resolution"]["width"] = conf.get("resolution").get("width")
            self._conf["resolution"]["height"] = conf.get("resolution").get("height")

    def dict(self):
        return self._conf

    def yaml(self):
        return yaml.dump(self.dict())

    def update(self, section, key, value):
        self._conf[section][key] = value

    def update_and_save(self, section, key, value):
        self.update(section, key, value)
        self.save()


config = Config()
