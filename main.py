from os import path
from shared.config import config

if __name__ == "__main__":
    # loading default config and loading it from file if it exists
    # otherwise creating a new config file
    config.load("config.yaml")
