from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import subprocess
import os


@dataclass
class ScreenInfo:

    name: str
    pid: int
    start_date: str
    start_time: str
    state: ScreenState

    def __str__(self) -> str:
        bottom_str: str = "="*len(self.name)+"================"
        return f"""
        ======= {self.name} =======
        PID: {self.pid}
        Start Date: {self.start_date}
        Start Time: {self.start_time}
        State: {self.state.value}
        {bottom_str}
        """


class ScreenState(Enum):
    DETACHED = "(Detached)"
    ATTACHED = "(Attached)"
    DEAD = "(DEAD ???)"

    def valueOf(value: str):
        for state in ScreenState:
            if state.value == value:
                return state
        return None


def parse_screen_list() -> list[ScreenInfo]:
    screens = subprocess.Popen(['screen', '-ls'], stdout=subprocess.PIPE)
    stdout, _ = screens.communicate()
    screen_info = stdout.decode('utf-8')
    # This occurs under the event where there are no screens
    if "No Sockets found" in screen_info:
        return []
    
    # This occurs under the event where there is screens running
    screens_text = screen_info.split("\r\n")[1:-1][0]

    screens_formatted = screens_text.split("\n")
    # Removes the last element which doesn't contain any information
    screens_formatted.pop()

    screens_info: list[ScreenInfo] = []
    for screen_text in screens_formatted:

        tab_splits = screen_text.split("\t")
        # First element is always empty
        tab_splits.pop(0)

        # Now First element is pid/name
        # We need to split it and get those values
        pid_split: list[str] = tab_splits[0].split(".")
        pid: int = int(pid_split[0])
        name: str = pid_split[1]

        # Second element is date/time
        date_time_split: list[str] = tab_splits[1].replace(
            "(", "").replace(")", "").split(" ")
        start_date: str = date_time_split[0]
        start_time: str = date_time_split[1]+" "+date_time_split[2]

        screens_info.append(ScreenInfo(
            name, pid, start_date, start_time, ScreenState.valueOf(tab_splits[2])))

    return screens_info


ACTIVE_SCREENS: list[ScreenInfo] = parse_screen_list()


def update_active_screens():
    global ACTIVE_SCREENS
    ACTIVE_SCREENS = parse_screen_list()


def get_parsed_screen(name: str) -> ScreenInfo:
    for screen in ACTIVE_SCREENS:
        if screen.name == name:
            return screen


def get_parsed_screen_by_pid(pid: int) -> ScreenInfo:
    for screen in ACTIVE_SCREENS:
        if screen.pid == pid:
            return screen


class Screen:

    screen_info: ScreenInfo
    running: bool

    def __init__(self, pid: int = None, name: str = None) -> None:
        if pid is not None:
            self.screen_info = get_parsed_screen_by_pid(pid)
        elif name is not None:
            self.screen_info = get_parsed_screen(name)
            
            if self.screen_info is None:
                self.screen_info = ScreenInfo(name, -1, "", "", ScreenState.DEAD)
        else:
            raise Exception("No screen info provided")

        if self.screen_info is None:
            raise ScreenDoesNotExistException("Screen not found")
        
        if self.screen_info.state is not None:
            self.running = self.screen_info.state != ScreenState.DEAD
            return
        
        self.running = False

    def start(self) -> None:
        if self.running:
            print("Screen is already running more info below about the screen")
            print(self.screen_info)
            return
        self.running = True
        subprocess.Popen(["screen", "-dmS", self.screen_info.name])
        update_active_screens()
        self.screen_info = get_parsed_screen(self.screen_info.name)

    def kill(self) -> None:
        if not self.running:
            print("Screen is not running")
            return
        self.running = False
        subprocess.Popen(["screen", "-X", "-S", self.screen_info.name, "quit"])
        update_active_screens()

    def attach(self) -> None:
        if not self.running:
            print("Screen is not running")
            return
        os.system(f"screen -r {self.screen_info.name}")


class ScreenDoesNotExistException(Exception):
    pass


if __name__ == "__main__":
    screen = Screen(name="test")
    screen.start()
