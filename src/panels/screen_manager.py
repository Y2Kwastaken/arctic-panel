from native_components.panel import Panel
from utils.cosmetics import cfiglet, cprint, cinput
from native_components.screen import Screen, get_all_screen_names
from pick import pick


class ScreenManager(Panel):

    def __init__(self, parent_panel: Panel, autoclear=True) -> None:
        options = {
            "1": ["Start a screen", self.start_screen],
            "2": ["Attach to a screen", self.attach_screen],
            "3": ["Send command to screen", self.send_command],
            "4": ["Kill screens", self.kill_screen],
        }
        super().__init__(options=options, parent_panel=parent_panel, autoclear=autoclear)
        super().start()

    def display_figlet(self):
        cfiglet("&b", "Screen Manager")

    def display_description(self):
        cprint("&fallows you to manage screens quickly and conveniently")

    def get_tag(self):
        return "SCM"

    def start_screen(self):
        screen_name = cinput(
            "&bEnter the name of the screen you want to start >> ")
        auto_attach = cinput(
            "&bDo you want to automatically attach to the new screen? (true / [false] ) >> ") or "false"
        screen: Screen = Screen(name=screen_name)
        screen.start()

        if auto_attach == "true":
            screen.attach()

    def attach_screen(self):
        all_screen_names: list[str] = get_all_screen_names()

        if len(all_screen_names) == 0:
            cinput("&cThere are no screens to attach to press enter to continue >> ")
            return

        attach_picker = pick(
            all_screen_names, "Select a screen to attach to", indicator="⟶", multiselect=False)
        screen: Screen = Screen(name=attach_picker[0])
        if screen.running:
            screen.attach()
        else:
            cinput(
                "&cThis screen is not running it may be dead??? Press enter to continue >> ")

    def kill_screen(self):
        all_screen_names: list[str] = get_all_screen_names()

        if len(all_screen_names) == 0:
            cinput("&cThere are no screens to kill press enter to continue >> ")
            return

        kill_picker = pick(
            all_screen_names, "Select screen names to kill", indicator="⟶", multiselect=True)
        for screen_name in kill_picker:
            screen: Screen = Screen(name=screen_name[0])
            screen.kill()
            cprint("&cKilled screen &b{}".format(screen_name))
        cinput("&cPress enter to continue >> ")

    def send_command(self):
        all_screen_names: list[str] = get_all_screen_names()

        if len(all_screen_names) == 0:
            cinput(
                "&cThere are no screens to send commands to press enter to continue >> ")
            return

        send_picker = pick(
            all_screen_names, "Select a screen to send commands to", indicator="⟶", multiselect=False)
        screen: Screen = Screen(name=send_picker[0])
        if screen.running:
            command: str = cinput(
                "&bEnter the command you want to send to the screen >> ")
            screen.send_command(command=command)
        else:
            cinput(
                "&cThis screen is not running it may be dead??? Press enter to continue >> ")
