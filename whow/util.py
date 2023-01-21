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
import math

from dataclasses import dataclass
from .colors import Color, Colors, Styles, get_color_class_from_name

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
    color: Color = Colors.white()

    def get_dictionary(self) -> dict[str, str]:
        return {
            "name": self.name.lower(),
            "color": self.color.name,
        }
    
    def __repr__(self) -> str:
        return f"{self.color.fg}{Colors.fg_end}{self.color.bg}{Styles.bold}{self.name} {Styles.end} {Colors.bg_end}"

@dataclass
class ToDoEntry():
    name: str
    due: datetime.date | None
    categories: list[Category]
    overdue: bool = False
    index: int = 0

    def get_dictionary(self) -> dict[str, str | bool | list[dict[str, str]]]:
        """
        Get a dictionary for writing TOMLs with.
        """

        due = f"{self.due.day}/{self.due.month}/{self.due.year}" if self.due is not None else 'N.A.'
        return {
            "name": self.name,
            "due": due,
            "categories": [c.get_dictionary() for c in self.categories],
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
    print(f"{Styles.bold}{Colors.yellow().colorprint('[>>]', return_string=True)}{Styles.end} {text}")

def error(text: str) -> None:
    print(f"{Styles.bold}{Colors.red().colorprint('[!!]', return_string=True)}{Styles.end} {text}")

def warn(text: str) -> None:
    print(f"{Styles.bold}{Colors.magenta().colorprint('[!!]', return_string=True)}{Styles.end} {text}")


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


def parse_category_from_dict(d: dict[str, str]) -> Category:
    """
    Parse a dictionary that was parsed from a `Category` back into a `Category`.
    """

    return Category(
        d["name"],
        get_color_class_from_name(d["color"])
    )
    
def parse_todoentry_from_dict(d: dict[str, dict[str, str | bool | list[dict[str, str]]]], file_name: str):
    """
    Parse a dictionary that was parsed from a `ToDoEvent` into a `ToDoEvent`.
    `file_name` should be the name of the file WITHOUT the extension.
    """

    unparsed_due = str(d[file_name]["due"]).split("/")
    due = datetime.date(int(unparsed_due[2]), int(unparsed_due[1]), int(unparsed_due[0]))
    return ToDoEntry(
        str(d[file_name]["name"]),
        due,
        [parse_category_from_dict(c) for c in d[file_name]["categories"]], # type: ignore
        overdue=True if type(d[file_name]["overdue"]) == True and d[file_name]["overdue"] else False,
        index=d[file_name]["index"] # type: ignore
    )
    
def _fill_idx(l: list[int | str]) -> tuple[list[int | str], int]:
    """
    fill an index.toml indexes list.
    This function is to bypass the use
    of a for-else clause, which is
    deprecated.
    """
    retval = []
    idx = 0
    found_spot = False

    for count, i in enumerate(l):
        retval.append(count)
        print(f"appended {count}, {i} at {count}")
        if i == "None":
            found_spot = True
            idx = count
    
    if not found_spot:
        retval.append(len(retval))
        idx = len(retval) - 1
    
    return (retval, idx)

def register_todo(todo_entry: ToDoEntry, force: bool = False) -> str | None:
    """
    Register a new To-Do.
    
    `force` is set to False as default, as
    ```py
    force=True
    ```
    will overwrite any todos with the same name
    as the current one!
    """

    if os.path.exists(os.path.join(os.environ['HOME'], f"./.local/whow/todos/{todo_entry.name}.toml")):
        if not force:
            warn("A to-do entry with the same name exists. Aborting.")
            return
        warn("A to-do entry with the same name already exists. Overwriting.")

    # load the used indexes
    with open(os.path.join(os.environ['HOME'], "./.local/whow/todos/index.toml")) as indexes:
        idx: list[int | str] = toml.loads(indexes.read())['indexes']
    
    todo_idx = _fill_idx(idx)
    print(todo_idx)

    # write new index.toml
    with open(os.path.join(os.environ['HOME'], "./.local/whow/todos/index.toml"), "w") as indextoml:
        indextoml.write(toml.dumps({
            "indexes": todo_idx[0]
        }))

    # write the todo toml file
    with open(os.path.join(os.environ['HOME'], f'./.local/whow/todos/{todo_entry.name}.toml'), "w+") as tml:
        # unwrap the optional
        todo_entry_due = todo_entry.due if todo_entry.due is not None else datetime.datetime.now()
        
        t = toml.dumps(
            {
                todo_entry.name: {
                    "index": todo_idx[1],
                    "name": todo_entry.name,
                    "due": f"{todo_entry.due.day}/{todo_entry.due.month}/{todo_entry.due.year}"
                           if todo_entry.due is not None else
                           f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}",
                    "categories": [c.name for c in todo_entry.categories],
                    "overdue": False if datetime.datetime.now() < todo_entry_due else True
                }
            }
        )
        tml.write(t)

    return f"Registered New To-Do: \n{t}"

def init_todos(destroy: bool = False):
    """
    Create the necessary paths for the To-Dos and Events.
    """

    if destroy:
        warn("Overwriting ~/.local/whow...")
        shutil.rmtree(os.path.join(os.environ['HOME'], './.local/whow'))

    # create dirs
    dirs = ["./.local/whow",
            "./.local/whow/todos",
            "./.local/whow/categories",
            "./.local/whow/events"]

    for dir in dirs:
        if not os.path.isdir(os.path.join(os.environ['HOME'], dir)):
            os.mkdir(os.path.join(os.environ['HOME'], dir))

    indextoml_tmp = toml.dumps(
        {
            "indexes": []
        }
    )

    # write the index.toml's
    todos_indextoml = open(os.path.join(os.environ['HOME'], './.local/whow/todos/index.toml'), "w+")
    events_indextoml = open(os.path.join(os.environ['HOME'], './.local/whow/events/index.toml'), "w+") 
    todos_indextoml.write(indextoml_tmp)
    events_indextoml.write(indextoml_tmp)

    todos_indextoml.close()
    events_indextoml.close()

def split_string_date(string_date: str) -> datetime.date:
    """
    Split a string date in the date/month/year format into a datetime.date object.
    """
    string_date_array = string_date.split("/")
    if (int(string_date_array[0]) > 31) or (int(string_date_array[1]) > 12):
        error("The date you supplied was invalid! It has to follow the date/month/year format.")
        exit()
    
    return datetime.date(int(string_date_array[2]), int(string_date_array[1]), int(string_date_array[0]))

def check_category_existence(name: str) -> bool:
    for path in os.listdir(os.path.join(os.environ['HOME'], f"./.local/whow/categories")):
        if (name == os.path.splitext(path)[0]) or (name.lower() == os.path.splitext(path)[0].lower()):
            return True
    return False

def match_name_with_category(name: str) -> Category:
    for path in os.listdir(os.path.join(os.environ['HOME'], f"./.local/whow/categories")):
        with open(os.path.join(os.environ['HOME'], "./.local/whow/categories", path), "r") as category_from_path:
            return parse_category_from_dict(toml.loads(category_from_path.read()))
    return Category("zombie_category")


def register_category(category: Category, force: bool = False) -> str | None:
    """
    Register a new category
    """
    if os.path.exists(os.path.join(os.environ['HOME'], f"./.local/whow/categories/{category.name}")):
        if not force:
            warn("A category entry with the same name exists. Aborting")
            return
        warn("A category entry with the same name already exists. Overwriting")
    
    with open(os.path.join(os.environ['HOME'], f'./.local/whow/categories/{category.name}.toml'), "w+") as categorytoml:
        t = toml.dumps(category.get_dictionary())
        categorytoml.write(t)

    return f"Wrote a new category toml. \n{t}"

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