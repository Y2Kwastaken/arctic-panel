'''
This file represents the spigot_resources.json file
this file is read only
'''
from os.path import dirname as parent
from utils.config import load_config, save_config


class ResourceData:

    config: any
    spigot_resources: dict
    bungee_resources: dict

    def __init__(self) -> None:
        self.config = load_config(
            f"{parent(parent(parent(__file__)))}/resources/spigot_resources.json")
        self.spigot_resources = self.config["spigot-resources"]
        self.bungee_resources = self.config["bungee-resources"]