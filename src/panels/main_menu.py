from panels.server_creator import ServerCreator
from panels.server_manager import ServerManager
from panels.screen_manager import ScreenManager
from utils.cosmetics import cfiglet, cprint
from native_components.panel import Panel


class MainMenu(Panel):

    def __init__(self, autoclear=True) -> None:
        options = {
            "1": ("Server Manager", self.server_manager),
            "2": ("Server Creator", self.server_creator),
            "3": ("Screen Manager", self.screen_manager),
        }
        super().__init__(options=options, autoclear=autoclear)
        super().start()

    def display_figlet(self):
        cfiglet("&3", "Arctic Panel")

    def display_description(self):
        cprint(
            "&7Arcitc Panel is a simple tool for managing Your VPS and Minecraft Servers")

    def get_tag(self):
        return "MM"
    
    def server_creator(self):
        ServerCreator(parent_panel=self)
    
    def server_manager(self):
        ServerManager(parent_panel=self)
        
    def screen_manager(self):
        ScreenManager(parent_panel=self)
