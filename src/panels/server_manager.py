
from native_components.minecraft_server import MinecraftServer
from native_components.servers_helper import ServersHelper
from utils.cosmetics import cfiglet
from native_components.panel import Panel
from native_components.screen import get_all_screen_names
from utils.cosmetics import cprint, cinput
from pick import pick


class ServerManager(Panel):

    shelper: ServersHelper

    def __init__(self, parent_panel: Panel = None) -> None:
        self.shelper = ServersHelper()

        options = {
            "1": ["Start Servers", self.start_servers],
            "2": ["Stop Servers", self.stop_servers],
            "3": ["Attach to Server", self.attach_server],
        }

        super().__init__(options=options, parent_panel=parent_panel)
        super().start()

    def display_figlet(self):
        cfiglet("&d", "Server Manager")

    def display_description(self):
        print("Manage your servers here")

    def get_tag(self):
        return "SM"

    def start_servers(self):
        
        offline_servers = self.offline_servers()

        if len(offline_servers) == 0:
            cinput("&cNo servers found to start... Press enter to continue >> ")
            return
        
        startable_servers = pick(
            offline_servers, "Select Servers to Start", indicator="⟶", multiselect=True)
        for server in startable_servers:
            MinecraftServer(server[0]).start()
            cprint(f"&aStarted {server[0]}")
    
    def stop_servers(self):
        
        online_servers = self.online_servers()
        if len(online_servers) == 0:
            cinput("&cNo servers found to stop... Press enter to continue >> ")
            return
        
        stoppable_servers = pick(
            online_servers, "Select Servers to Stop", indicator="⟶", multiselect=True)
        for server in stoppable_servers:
            MinecraftServer(server[0]).stop()
            cprint(f"&aStopped {server[0]}")
    
    def attach_server(self):
        online_servers = self.online_servers()
        
        if len(online_servers) == 0:
            cinput("&cNo servers found to attach to... Press enter to continue >> ")
            return
        
        attach_picker = pick(online_servers, "Select Server to Attach To", indicator="⟶")
        MinecraftServer(attach_picker[0]).attach()
        
    
    def online_servers(self) -> list[str]:
        all_servers = self.shelper.all_minecraft() + self.shelper.all_proxies()

        all_screen_names: list[str] = get_all_screen_names()
        for server in all_servers:

            # Checks if the server is already running via screen
            if server not in all_screen_names:
                all_servers.remove(server)

        return all_servers

    def offline_servers(self) -> list[str]:
        all_servers = self.shelper.all_minecraft() + self.shelper.all_proxies()

        all_screen_names: list[str] = get_all_screen_names()
        for server in all_servers:

            # Checks if the server is already running via screen
            if server in all_screen_names:
                all_servers.remove(server)

        return all_servers