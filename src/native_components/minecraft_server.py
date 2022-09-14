from re import S
from configs.config_manager import CONFIG
from native_components.screen import Screen
from utils.cosmetics import cprint
from utils.killable_thread import thread_with_trace
from os import path
import time
import os


EXIT_CONSOLE_PHRASES = ["exit", "e", "back", "b", "quit", "q", "leave", "l"]
STOP_SERVER_PHRASES = ["stop", "shutdown"]
RESTART_SERVER_PHRASES = ["restart", "reboot"]
BLACK_LISTED_COMMANDS = CONFIG.blacklisted_commands


class MinecraftServer():

    path: str
    screen: Screen
    running: bool

    def __init__(self, server_name: str) -> None:
        self.path = f"{CONFIG.server_directory}/{server_name}"
        self.screen = Screen(name=server_name)
        self.running = self.screen.running

    def start(self):

        if self.running:
            cprint("&cServer is already running unable to start")
            return

        self.screen.start()
        self.screen.send_command(f"cd {self.path}")
        self.screen.send_command("./start.sh")
        self.running = True

    def stop(self):

        if not self.running:
            cprint("&cServer is not running unable to shutdown")
            return

        self.screen.send_command(f"stop")
        self.screen.kill()

    def restart(self):
        cprint("&cRestarting server")
        self.stop()
        self.start()
        cprint("&aServer restarted")

    def attach(self):
        console = thread_with_trace(target=self.follow)
        console.start()
        attached = True

        cprint("&3You are now attached to the server console")
        self.panel_help()
        while attached:
            user_input = input()
            if user_input in EXIT_CONSOLE_PHRASES:
                attached = False
            elif user_input == "panel-help":
                self.panel_help()
            elif user_input in STOP_SERVER_PHRASES:
                self.stop()
                attached = False
            elif user_input in RESTART_SERVER_PHRASES:
                self.restart()
            elif user_input in BLACK_LISTED_COMMANDS:
                cprint("&cThis command is blacklisted by the panel and cannot be used")
                cprint(
                    "&cif you belive this is a mistake contact an administrator or edit the config.json file")
            else:
                self.screen.send_command(user_input)

        console.kill()
        console.join(timeout=0.05)

    def follow(self) -> None:
        log_location = f"{self.path}/logs/latest.log"
        if not path.isfile(log_location):
            cprint("&cUnable to find any log file manually creating one")
            # Manually create a log file
            with open(log_location, "x") as f:
                f.close()
            return

        with open(log_location, "r") as log:
            log.seek(0, os.SEEK_END)

            while True:
                line = log.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                cprint(line.replace("\n", ""))

    def panel_help(self) -> None:
        print()
        cprint("&cPanel Commands: ")
        print()
        cprint("&cType &epanel-help &cto view this message")
        cprint("&cType &eexit or e &c to exit the console")
        cprint("&cType &estop or shutdown &c to shutdown the server")
        cprint("&cType &erestart or reboot &c to restart the server")
        print()
        cprint("&7This panel can also &cblacklist &7commands from being used")
        cprint("&7to add a command to the blacklist edit the config.json file")
        print()
        cprint("&7The following commands are blacklisted:")
        cprint(f"&e{BLACK_LISTED_COMMANDS}")
        print()
        