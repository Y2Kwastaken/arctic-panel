import os
import requests
import shutil
from pick import pick
from tqdm import tqdm
from typing import Union
from configs.config_manager import CONFIG, RESOURCE_CONFIG
from http.client import HTTPException

SPIGET_LINK = 'https://api.spiget.org/v2/resources/{id}/download'


def chdir(dir) -> str:
    '''
    A better version of os.chdir
    '''
    wd = os.getcwd()
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print(f'created directory at {dir}')
        os.chdir(dir)
    else:
        os.chdir(dir)
    return wd


def download(link, name=None, return_json=False, no_download=False) -> Union[int, any]:
    '''
    Downloads a file
    '''
    wd = chdir(CONFIG.cache_directory)
    data = requests.get(link)

    if not no_download:
        if name == None:
            name = link.split("/")[-1]

        with open(name, 'wb') as f:
            f.write(data.content)
        os.chdir(wd)

    if data.status_code == 404:
        raise HTTPException(link, data.status_code, data.reason)

    if return_json:
        return data.status_code, data.json()

    return data.status_code, None


def spiget_download(id: int, name: str, path=os.getcwd()) -> None:
    response = requests.get(SPIGET_LINK.format(id=id), stream=True)
    total = int(response.headers.get('content-length'))

    jar_file = f"{path}/{name}.jar"

    with open(jar_file, 'wb') as file, tqdm(
        desc=name,
        total=total,
        unit='MiB',
        unit_scale=True,
        unit_divisor=1024,
        # https://github.com/tqdm/tqdm/issues/585
        bar_format="{l_bar}{bar:10}{r_bar}{bar:-10b}"
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def install_resource(server_name: str, spigot: bool = True) -> None:

    plugins_folder: str = f"{CONFIG.server_directory}/{server_name}/plugins"

    if spigot:
        choices = pick(list(RESOURCE_CONFIG.spigot_resources.keys(
        )), "Select resourcs to install", multiselect=True, indicator='⟶')
        install_spigot_resource(plugins_folder, choices)
    else:
        choices = pick(list(RESOURCE_CONFIG.spigot_resources.keys(
        )), "Select resources to install", multiselect=True, indicator='⟶')
        install_bungee_resource(plugins_folder, choices)


def install_spigot_resource(plugins_folder: str, choices: list):
    '''
    Installs spigot resources
    '''
    for choice in choices:

        plugin_name = choice[0]
        entry_value = RESOURCE_CONFIG.spigot_resources[plugin_name]

        if "local:" in str(entry_value):
            shutil.copyfile(entry_value.replace("local:", ""),
                            f"{plugins_folder}/{plugin_name}.jar")
        else:
            spiget_download(entry_value, plugin_name, plugins_folder)

def install_bungee_resource(plugins_folder: str, choices: list):
    '''
    Installs bungeecord resources
    '''
    pass
