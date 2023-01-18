#    Whow 
#    A rewrite of DaringCuteSeal/whow in Python that aims to polish the overall UX.

#    Copyright (C) 2023 ezntek (ezntek@xflymusic.com) and DaringCuteSeal (daringcuteseal@gmail.com)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.

import datetime
import toml
import os
import shutil
import colorama
import math

from dataclasses import dataclass

# class definitions
@dataclass
class EventDateTime():
    date: datetime.date
    time: datetime.time

    def __repr__(self) -> str:
        return f"{self.date.day}/{self.date.month}/{self.date.year} {self.time.hour}:{self.time.minute}:{self.time.second}"
@dataclass
class Category():
    name: str
    color: str = colorama.Back.RESET # colorama color

    def get_dictionary(self) -> dict[str, str]:
        return {
            "name": self.name,
            "color": self.color,
        }
    
    def __repr__(self) -> str:
        return f"{colorama.Fore.RED}{colorama.Fore.RESET}{colorama.Back.RED} {colorama.Style.BRIGHT}{self.name} {colorama.Style.RESET_ALL} {colorama.Back.RESET}"

@dataclass
class ToDoEntry():
    name: str
    due: datetime.date | None
    categories: list[Category]
    overdue: bool = False

    def get_dictionary(self) -> dict[str, str | list[str | None]]:
        due = f"{self.due.day}/{self.due.month}/{self.due.year}" if self.due is not None else 'N.A.'
        return {
            "name": self.name,
            "due": due,
            "categories": [c.name for c in self.categories],
            "overdue": self.overdue.__repr__()
        }
    
@dataclass
class EventEntry():
    name: str
    event_from: EventDateTime
    event_to: EventDateTime | None
    description: str
    full_day: bool = False

    def get_dictionary(self) -> dict[str, str | bool | None]:
        return {
            "name": self.name,
            "full_day": self.full_day,
            "from": self.event_from.__repr__(),
            "to": self.event_to.__repr__() if self.event_to is not None else "",
            "description": self.description
        }

# Function Definitions
def log(text: str) -> None:
    print(f"{colorama.Fore.YELLOW}{colorama.Style.BRIGHT}[>>]{colorama.Style.RESET_ALL} {text}")

def error(text: str) -> None:
    print(f"{colorama.Back.RED}{colorama.Style.BRIGHT}{colorama.Fore.WHITE}[!!]{colorama.Style.RESET_ALL} {text}")

def warn(text: str) -> None:
    print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}[!!]{colorama.Style.RESET_ALL} {text}")


def indexify_weekday(weekday: int) -> int:
    """
    Converts the 0==Monday, 6==Sunday dates
    from *.weekday() to 0==Sunday, 6==Saturday dates
    """

    match weekday:
        case 6:
            return 0
        case _:
            return weekday+1

def fprint(string: str, padding: int = 1, flowtext: bool = True) -> None:
    """
    Print out a string, omitting overflowed text based
    on the terminal width.
    """

    term_width = shutil.get_terminal_size().columns - 2 - padding
    overflow = '…' if flowtext and (len(string) + padding) > term_width else ''
    text_padding: str = " "*padding

    print(f"{text_padding}{string[0:term_width]}{overflow}")

def print_center(string: str, width: int, bias_left: bool = True, return_string: bool = False) -> None | str:
    """
    Center out a string in a given area (width: int)
    and print that string in the center of that area.
    If the total padding is odd, set the bias variable
    to either "left" or "right" to give one more whitespace
    to that direction.
    """

    padding_width = width - len(string)

    if padding_width % 2 == 1: # check for if padding_width is odd
        # Calculate the padding based on the kwarg
        l_padding_width = math.ceil(padding_width/2) if bias_left else math.floor(padding_width/2)
        r_padding_width = padding_width - l_padding_width

        # print
        if return_string:
            return f"{' '*l_padding_width}{string}{' '*r_padding_width}"
        print(f"{' '*l_padding_width}{string}{' '*r_padding_width}")
    elif padding_width % 2 == 0:
        if return_string:
            return f"{' '*int(padding_width/2)}{string}{' '*int(padding_width/2)}"
        print(f"{' '*int(padding_width/2)}{string}{''*int(padding_width/2)}")

def register_todo(todo_entry: ToDoEntry, force: bool = False):
    """
    Register a new To-Do.
    """

    


def init_todos(destroy: bool = False):
    """
    Create the necessary paths for the To-Dos and Events.
    """
    
    if destroy:
        shutil.rmtree(os.path.join(os.environ['HOME'], './.local/whow'))

    dirs = ["./.local/whow",
            "./.local/whow/todos",
            "./.local/whow/events"]

    for dir in dirs:
        if not os.path.isdir(os.path.join(os.environ['HOME'], dir)):
            os.mkdir(os.path.join(os.environ['HOME'], dir))

def new_config(destroy: bool = False) -> str:
    """
    Create a new config file.
    """

    # create dirs if they don't exist
    if not os.path.isdir(os.path.join(os.environ['HOME'], "./.config/whow")):
        os.mkdir(os.path.join(os.environ['HOME'], "./.config/whow"))

    if not os.path.isdir(os.path.join(os.environ['HOME'], "./.config")):
        os.mkdir(os.path.join(os.environ['HOME'], "./.config"))
     
    # generate a config and write
    try:
        if destroy:
            os.remove(os.path.join(os.environ['HOME'], './.config/whow/config.toml'))
    except OSError:
        pass

    c: str = toml.dumps({
            "config": {
                "default_separator": "line",
                "enable_emojis": True,
            }
        })

    with open(os.path.join(
        os.environ['HOME'], './.config/whow/config.toml'
    ), "w+") as cfg:
        cfg.write(c)
    
    return f"Dumped toml successfully. \n{c}"