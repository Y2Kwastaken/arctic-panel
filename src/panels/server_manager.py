
from utils.cosmetics import cfiglet
from utils.panel import Panel


class ServerManager(Panel):

    def __init__(self, parent_panel: Panel = None) -> None:
        options = {

        }

        super().__init__(options=options, parent_panel=parent_panel)
        super().start()
    
    def display_figlet(self):
        cfiglet("&d", "Server Manager")
    
    def display_description(self):
        print("Manage your servers here")
    
    def get_tag(self):
        return "SM"
    

class Server:
    
    name: str
    path: str
    running: bool
