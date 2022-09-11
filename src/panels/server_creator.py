from os import mkdir, system
from os.path import isdir
from configs.config_manager import CONFIG
from random import randint
from utils.panel import Panel
from utils.file import install_resource
from utils.cosmetics import cfiglet, cinput, cprint
from utils.server_install import install_paper, install_waterfall
from utils.servers_helper import ServersHelper, ServersHelper
from pick import pick
import shutil


class ServerCreator(Panel):

    shelper: ServersHelper

    def __init__(self, parent_panel: Panel = None, autoclear=True) -> None:
        self.shelper = ServersHelper()
        options = {
            "1": ("Create a PaperMC Server", self.paper),
            "2": ("Create a Waterfall Server", self.waterfall),
        }
        super().__init__(options=options, parent_panel=parent_panel, autoclear=autoclear)
        super().start()

    def display_figlet(self):
        cfiglet("&b", "Server Creator")

    def display_description(self):
        print("")

    def paper(self):
        PaperServerCreator(self.shelper)

    def waterfall(self):
        install_waterfall()


class PaperServerCreator():

    shelper: ServersHelper

    def __init__(self, shelper: ServersHelper) -> None:
        self.shelper = shelper

        jar = install_paper()
        rnum = randint(30_000, 35_000)
        servername = cinput(
            "&bEnter a name for the server (default: {}) &b>> ".format(f"myserver-{rnum}")) or f"myserver-{rnum}"
        ram = cinput("&fEnter the amount of ram (default: 4G) &b>> ") or "4G"

        if isdir(servername):
            cprint("&cThis server already exists exitting...")
            return

        mkdir(CONFIG.server_directory+"/"+servername)

        create_start_script(ram, servername, jar)
        self.create_configs(servername)
        install_resource(servername)

    def create_configs(self, server_name):

        port_invalid = True
        while port_invalid:
            port: int = int(
                cinput("&bEnter the desired port (default: 25565) &b>> ") or "25565")
            if not self.shelper.port_in_use(port):
                break

        allow_end: str = cinput("&bAllow end? (default: true) &b>> ") or "true"
        allow_nether: str = cinput(
            "&bAllow nether? (default: true) &b>> ") or "true"
        max_players: str = cinput(
            "&bEnter the max players (default: 20) &b>> ") or "20"
        view_distance: str = cinput(
            "&bEnter the view distance (default: 10) &b>> ") or "10"
        advancements: str = cinput(
            "&bAllow advancements? (default: true) &b>> ") or "true"
        behind_bungee: str = cinput(
            "&bBehind bungee? (default: false) &b>> ") or "false"

        server_path = f"{CONFIG.server_directory}/{server_name}"

        with open(f"{server_path}/server.properties", 'a') as properties:
            properties.write(f"server-port={str(port)}\n")
            properties.write(f"allow-nether={allow_nether}\n")
            properties.write(f"max-players={max_players}\n")
            properties.write(f"view-distance={view_distance}\n")

            if (behind_bungee == "true"):
                picked = pick(self.shelper.all_proxies(),
                              "Select a proxy to use", multiselect=False)
                self.shelper.add_server_to_proxy(picked[0], server_name, port)
                properties.write(f"online-mode=false\n")
                properties.write(f"network-compression-threshold=-1\n")
            else:
                properties.write(f"online-mode=true\n")
                properties.write(f"network-compression-threshold=256\n")

        with open(f"{server_path}/spigot.yml", "a") as spigotyml:
            spigotyml.write(
                f"""settings:\n  bungeecord: {behind_bungee}\n  restart-on-crash: false\nadvancements:\n    disable-saving: {advancements}""")
        with open(f"{server_path}/bukkit.yml", "a") as bukkityml:
            bukkityml.write(f"""settings:\n  allow-end: {allow_end}""")


def create_start_script(ram: str, servername: str, jar: str):
    # Start file creation.
    script = f'''#!/bin/sh\n# Reecepbcups - start.sh script for servers. EULA Auto Accepted.\n\nMEM_HEAP="{ram}"\nJAR_FILE="{jar}"\n'''
    # If RAM usage is >12GB, optomized java arguments are used
    # remove all letters from RAM, so its only the #
    if 'g' in ram.lower() and int(''.join(filter(str.isdigit, ram))) > 12:
        script += 'JAVA_ARGS="-Dfile.encoding=utf-8 -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=40 -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:-OmitStackTraceInFastThrow -XX:+AlwaysPreTouch  -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=8 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=true -Daikars.new.flags=true -Dcom.mojang.eula.agree=true"'
    else:
        script += 'JAVA_ARGS="-Dfile.encoding=utf-8 -Dcom.mojang.eula.agree=true"'

        script += f'''\n\nwhile true; do\n\tjava -Xms$MEM_HEAP -Xmx$MEM_HEAP $JAVA_ARGS -jar $JAR_FILE nogui\n\techo "Restarting server in 5 seconds"\n\tsleep 4\n\techo "Restarting..."\n\tsleep 1\ndone'''
        # write startFile to test.sh
        server_path = CONFIG.server_directory+"/"+servername
        with open(server_path+'/start.sh', 'w') as file:
            file.write(script)
            # print("start.sh file made")
        system(f"chmod +x {server_path}/start.sh")
