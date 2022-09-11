from configs.config_manager import CONFIG
from utils.config import load_yaml_config, load_properties, save_yaml_config
from utils.cosmetics import cinput, cprint
from cachetools import cached, TTLCache

from configs.config_manager import CONFIG
from cachetools import cached, TTLCache
from os import listdir
from os.path import isfile
import yaml

proxy_config_cache: TTLCache = TTLCache(maxsize=10, ttl=360)
server_properties_cache: TTLCache = TTLCache(maxsize=10, ttl=360)


class ServersHelper():

    @cached(proxy_config_cache)
    def get_proxy_config(self, proxy_name: str) -> any:
        return load_yaml_config(CONFIG.server_directory+"/"+proxy_name+"/config.yml")

    @cached(server_properties_cache)
    def get_server_properties(self, server_name: str) -> any:
        return load_properties(CONFIG.server_directory+"/"+server_name+"/server.properties")

    def port_in_use(self, port: int) -> bool:

        for directory in listdir(CONFIG.server_directory):
            if self.get_port(directory) == port:
                cprint("&cPort {} is already in use by {}".format(port, directory))
                return True
                
        return False

    def add_server_to_proxy(self, proxy_name: str, server_name: str, port: int) -> None:
        motd: str = cinput("&bEnter the motd for the server: ")
        address: str = cinput(
            "&bEnter the IP address of the server (default: 127.0.0.1) >> ") or "127.0.0.1"
        restricted: str = cinput(
            "&bRestricted? (defualt: false) >> ") or "false"

        proxy_config = self.get_proxy_config(proxy_name)
        proxy_config["servers"][server_name] = dict(
            motd=motd, address=address+":"+str(port), restricted=restricted)
        save_yaml_config(proxy_config, CONFIG.server_directory +
                         "/"+proxy_name+"/config.yml")

    def get_port(self, directory) -> int:
        if self.is_proxy(directory):
            return int(self.get_proxy_config(directory)["listeners"][0]["host"].split(":")[1])
        elif self.is_minecraft(directory):
            return int(self.get_server_properties(directory)["server-port"])

    def all_proxies(self) -> list:
        proxies = []
        for directory in listdir(CONFIG.server_directory):
            if self.is_proxy(directory):
                proxies.append(directory)
        return proxies

    def all_minecraft(self) -> list:
        servers = []
        for directory in listdir(CONFIG.server_directory):
            if self.is_minecraft(directory):
                servers.append(directory)
        return servers

    def is_minecraft(self, server_name: str) -> bool:
        possible_eula = CONFIG.server_directory+"/"+server_name+"/eula.txt"
        return isfile(possible_eula)

    def is_proxy(self, proxy_name: str) -> bool:
        possible_config = CONFIG.server_directory+"/"+proxy_name+"/config.yml"
        return isfile(possible_config)
