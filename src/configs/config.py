'''
This file represents the config.json file
'''
from os.path import dirname as parent
from utils.config import load_config, save_config


class ConfigData:

    config: any  # I wish I knew waht type this was
    server_directory: str
    cache_directory: str
    blacklisted_commands: list[str]

    def __init__(self) -> None:
        self.config = load_config(
            f"{parent(parent(parent(__file__)))}/resources/config.json")

        self.server_directory = self.config["server-directory"]
        self.cache_directory = self.config["download-cache"]
        self.blacklisted_commands = self.config["blacklisted-commands"]

    def write(self, key: any, value: any):
        self.config[key] = value
    
    def save(self) -> None:
        save_config(
            self.config, f"{parent(parent(parent(__file__)))}/resources/config.json")
