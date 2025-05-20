import yaml
import os
from rich import print


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
            }
        }

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
