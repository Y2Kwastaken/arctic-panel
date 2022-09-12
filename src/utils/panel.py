from __future__ import annotations
from ast import Tuple

import os
from utils.cosmetics import cprint, cinput


class Panel:

    root: bool
    autoclear: bool
    options: dict
    parent: Panel

    layout: function

    def __init__(self, options: dict, layout: function = None, parent_panel: Panel = None, autoclear=True) -> None:
        self.autoclear = autoclear
        self.root = os.geteuid() == 0
        self.options = options
        self.parent = parent_panel

        self.layout = layout
        self.clear()

    def start(self):
        while True:

            self.panel_layout()

            uinput, possible_option = self.panel_input(self.get_tag())

            if possible_option:
                self.options[uinput][1]()

    def panel_layout(self) -> None:
        if self.layout is not None:
            self.layout()
            return

        self.display_figlet()
        self.display_description()
        print("")

        for k, v in self.options.items():
            cprint(f"[{k}] —> {v[0]}")

    def panel_input(self, in_style: str) -> Tuple(str, bool):
        '''
        Returns True if the user input is in the panel options 
        otherwise returns false and will fall back to panel 
        command selections
        '''
        uinput = cinput(f"\n{in_style}> ")

        if uinput == "back" or uinput == "b":
            cprint("&4Going back...")
            self.clear()
            if self.parent is not None:
                self.parent.start()
            else:
                cprint("&4No parent panel found to go back too...")
                cprint("&4Exiting...")
                exit(0)

        if uinput == "exit" or uinput == "e":
            cprint("&4Exiting...")
            exit(0)

        if len(uinput) == 0 or uinput not in self.options:
            self.clear()
            cprint("&4Invalid option")
            return uinput, False

        return uinput, True

    def display_figlet(self):
        raise NotImplementedError()

    def display_description(self):
        raise NotImplementedError()

    def get_tag(self) -> str:
        raise NotImplementedError()

    def clear(self):
        # Time differential on tests
        # os.system("clear") -> 0.0015304088592529297
        # print(\033c) -> 3.075599670410156e-05
        # Using a faster method leads to smoother and quick transitions from panel screen
        if (self.autoclear):
            print("\033c")
