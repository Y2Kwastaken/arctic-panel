from panels.server_creator import ServerCreator
from utils.cosmetics import cfiglet, cprint
from utils.panel import Panel


class MainMenu(Panel):

    def __init__(self, autoclear=True) -> None:
        options = {
            "2": ("Server Creator", self.server_creator),
        }
        super().__init__(options=options, autoclear=autoclear)
        super().start()

    def display_figlet(self):
        cfiglet("&3", "Arctic Panel")

    def display_description(self):
        cprint(
            "&7Arcitc Panel is a simple tool for managing Your VPS and Minecraft Servers")

    def server_creator(self):
        ServerCreator(parent_panel=self)