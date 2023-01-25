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
from colors import Color, Colors, Styles, get_color_class_from_name

# class definitions
@dataclass
class EventDateTime():
    date: datetime.date = datetime.datetime.now().date()
    time: datetime.time = datetime.datetime.now().time()

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
    ticked: bool = False
    index: int = 0

@dataclass
class EventEntry():
    name: str
    event_from: EventDateTime
    event_to: EventDateTime | None
    description: str
    categories: list[Category]
    full_day: bool = False
    index: int = 0

# Function Definitions
def log(text: str, return_string: bool = False) -> None | str:
    return f"{Styles.bold}{Colors.yellow().colorprint('[>>]', return_string=True)}{Styles.end} {text}" if return_string else print(f"{Styles.bold}{Colors.yellow().colorprint('[>>]', return_string=True)}{Styles.end} {text}")

def error(text: str, return_string: bool = False) -> None | str:
    return f"{Styles.bold}{Colors.red().colorprint('[!!]', return_string=True)}{Styles.end} {text}" if return_string else print(f"{Styles.bold}{Colors.red().colorprint('[!!]', return_string=True)}{Styles.end} {text}")

def warn(text: str, return_string: bool = False) -> None | str:
    return f"{Styles.bold}{Colors.magenta().colorprint('[!!]', return_string=True)}{Styles.end} {text}" if return_string else print(f"{Styles.bold}{Colors.magenta().colorprint('[!!]', return_string=True)}{Styles.end} {text}")


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

def get_eventdatetime_from_str(string: str) -> EventDateTime:
    l1 = string.split(" ") # ["d/m/y", "h:m:s"]
    date_split = l1[0].split("/")
    time_split = l1[1].split(":")
    return EventDateTime(datetime.date(int(date_split[2]), int(date_split[1]), int(date_split[0])), datetime.time(int(time_split[0]), int(time_split[1]), int(time_split[2])))

def parse_category_from_name(s: str) -> Category:
    """
    Parse a dictionary that was parsed from a `Category` back into a `Category`.
    """

    BASEDIR = os.path.join(os.environ['HOME'], "./.local/whow/categories")
    for category_filename in os.listdir(BASEDIR):
        c = toml.load(os.path.join(BASEDIR, category_filename))
        if c["name"] == s:
            return Category(
                s,
                get_color_class_from_name(c["color"])
            )
    raise NameError("The category name was not found! perhaps you did not add it yet?")

    
def parse_todoentry_from_dict(d: dict[str, dict[str, str | bool | list[dict[str, str]]]], file_name: str) -> ToDoEntry:
    """
    Parse a dictionary that was parsed from a `ToDoEntry` into a `ToDoEntry`.
    `file_name` should be the name of the file WITHOUT the extension.
    """

    unparsed_due = str(d[file_name]["due"]).split("/")
    due = datetime.date(int(unparsed_due[2]), int(unparsed_due[1]), int(unparsed_due[0]))
    return ToDoEntry(
        str(d[file_name]["name"]).replace("_", " "),
        due,
        [parse_category_from_name(c) for c in d[file_name]["categories"]], # type: ignore
        overdue=True if (type(d[file_name]["overdue"]) == True and d[file_name]["overdue"]) or (datetime.datetime.now().date() > due) else False,
        ticked=d[file_name]["ticked"], # type: ignore
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
        #print(f"appended {count}, {i} at {count}")
        if i == "None":
            found_spot = True
            idx = count
    
    if not found_spot:
        retval.append(len(retval))
        idx = len(retval) - 1
     
    return (retval, idx)

def pop_indextoml_element(element: int, type: str = "todos") -> None:
    """
    Remove an entry from an index.toml.
    """

    if type != "todos" and type != "events":
        type = "todos"
    
    with open(os.path.join(os.environ['HOME'], f"./.local/whow/{type}/index.toml"), "r") as index_toml:
        indexes: list[int | str] = toml.loads(index_toml.read())['indexes']
        for count, idx in enumerate(indexes):
            if idx == element:
                indexes[count] = "None"
    
    with open(os.path.join(os.environ['HOME'], f"./.local/whow/{type}/index.toml"), "w") as index_toml:
        index_toml.write(toml.dumps({
            "indexes": indexes
        }))

def match_todo_index(index: int) -> str:
    """
    Find a to-do filename based on its index.
    """

    BASEDIR = os.path.join((os.environ["HOME"]), f'./.local/whow/todos/')
    for filename in os.listdir(BASEDIR):
        if filename == "index.toml":
            continue
        data = toml.load(os.path.join(BASEDIR, filename))
        todo_name = os.path.splitext(filename.replace("_", " "))[0]

        if index == data[todo_name]["index"]:
            return filename
    raise IndexError('No file with this to-do index exists! Perhaps the index.toml is corrupted?')


def del_todo(index: int) -> str:
    """
    Delete a to-do by its index.
    """
    
    try:
        filename = match_todo_index(index)
    except IndexError:
        error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""
        
    BASEDIR = os.path.join((os.environ["HOME"]), f'./.local/whow/todos/')
    todo_name = os.path.splitext(filename.replace("_", " "))[0]
    todo = parse_todoentry_from_dict(toml.load(os.path.join(BASEDIR, filename)), os.path.splitext(filename)[0])
    
    if index == todo.index:
        os.remove(os.path.join(BASEDIR, filename))
        pop_indextoml_element(index)
        return f"Deleted to-do: {todo_name}\n"
    return ""

def mark_todo(index: int) -> str:
    """
    Tick a to-do as done/undone.
    """

    try:
        filename = match_todo_index(index)
    except IndexError:
        error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""

    data = toml.load(os.path.join((os.environ["HOME"]), f'./.local/whow/todos/', filename))
    todo_name = os.path.splitext(filename.replace("_", " "))[0]
    todo = parse_todoentry_from_dict(data, todo_name)
    
    todo.ticked = not todo.ticked
    register_todo(todo, force=True, quiet=True, use_old_index=True)
    
    return f"Marked to-do: {filename} as {not todo.ticked}\n" 

def register_todo(todo_entry: ToDoEntry, force: bool = False, quiet: bool = False, use_old_index: bool = False) -> str | None:
    """
    Register a new To-Do.
    
    `force` is set to False as default, as
    ```py
    force=True
    ```
    will overwrite any todos with the same name
    as the current one!

    ```py
    quiet=True
    ```
    will make the function "shut up".

    ```py
    use_old_index=True
    ```
    will keep the same index as the index provided
    by the `todo_entry.index` value, for use with
    certain functions only.
    """
    # replace all whitespaces with underscores
    todo_entry.name.replace(" ", "_")

    # guard clause
    if os.path.exists(os.path.join(os.environ['HOME'], f"./.local/whow/todos/{todo_entry.name}.toml")):
        if not force:
            warn("A to-do entry with the same name exists. Aborting.") if not quiet else None
            return
        warn("A to-do entry with the same name already exists. Overwriting.") if not quiet else None

    todo_idx = (0, 0)
    if not use_old_index:
        # load the used indexes
        with open(os.path.join(os.environ['HOME'], "./.local/whow/todos/index.toml")) as indexes:
            idx: list[int | str] = toml.loads(indexes.read())['indexes']
        
        todo_idx = _fill_idx(idx)

        # write new index.toml
        with open(os.path.join(os.environ['HOME'], "./.local/whow/todos/index.toml"), "w") as indextoml:
            indextoml.write(toml.dumps({
                "indexes": todo_idx[0]
            }))

    # write the todo toml file
    with open(os.path.join(os.environ['HOME'], f'./.local/whow/todos/{todo_entry.name.replace(" ", "_")}.toml'), "w+") as tml:
        # unwrap the optional
        todo_entry_due = todo_entry.due if todo_entry.due is not None else datetime.datetime.now().date()
        
        t = toml.dumps(
            {
                todo_entry.name: {
                    "index": todo_idx[1] if not use_old_index else todo_entry.index,
                    "name": todo_entry.name,
                    "due": f"{todo_entry.due.day}/{todo_entry.due.month}/{todo_entry.due.year}"
                           if todo_entry.due is not None else
                           f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}",
                    "categories": [c.name for c in todo_entry.categories],
                    "overdue": False if datetime.datetime.now().date() < todo_entry_due else True,
                    "ticked": todo_entry.ticked
                }
            }
        )
        tml.write(t)

    return f"Registered New To-Do: \n{t}"

def init_todos(destroy: bool = False) -> None:
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
        if os.path.splitext(path)[0] == name:
            try:
                return parse_category_from_name(toml.load(os.path.join(os.environ['HOME'], "./.local/whow/categories", path))['name'])
            except NameError:
                break
    raise NameError("The category name was not found! Perhaps you did not add it yet?")

def match_category_name_with_filename(name: str) -> str:
    """
    Find a filename based on the category name.
    """
    name = name.replace(" ", "_").lower()

    for n in os.listdir(os.path.join(os.environ['HOME'], f"./.local/whow/categories")):
        if n == f"{name}.toml":
            return(n)

    raise NameError("No category found with name!")

def register_category(category: Category, force: bool = False) -> str | None:
    """
    Register a new category
    """
    if os.path.exists(os.path.join(os.environ['HOME'], f"./.local/whow/categories/{category.name}")):
        if not force:
            warn("A category entry with the same name exists. Aborting")
            return
        warn("A category entry with the same name already exists. Overwriting")

    n = category.name.replace(" ", "_")

    with open(os.path.join(os.environ['HOME'], f'./.local/whow/categories/{n}.toml'), "w+") as categorytoml:
        t = toml.dumps(category.get_dictionary())
        categorytoml.write(t)

    return f"Wrote a new category toml. \n{t}"

def del_category(name: str) -> str:
    BASEDIR = os.path.join(os.path.join(os.environ['HOME'], f"./.local/whow/categories"))
    try:
        filename = match_category_name_with_filename(name)
        os.remove(os.path.join(BASEDIR, filename))
        return f"Deleted category: {name}"
    except NameError:
        error("A category with this name does not exist! please re-evaluate your input.")
    return ""
    

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

def register_event(event_entry: EventEntry, force: bool = False, quiet: bool = False, use_old_index: bool = False) -> str | None:
    event_entry.name.replace(" ", "_")

    if os.path.exists(os.path.join(os.environ['HOME'], f"./.local/whow/events/{event_entry.name}.toml")):
        if not force:
            warn("An event entry with the same name exists, aborting.") if not quiet else None
            return
        warn("An event entry with the same name already exists. Overwriting.") if not quiet else None
        
    event_idx = (0, 0)
    if not use_old_index:
        # load used indexes
        idx: list[str | int] = toml.load(os.path.join(os.environ['HOME'], "./.local/whow/events/index.toml"))['indexes']
        event_idx = _fill_idx(idx)

        # write the new index.toml
        with open(os.path.join(os.environ['HOME'], "./.local/whow/events/index.toml"), "w") as indextoml:
            toml.dumps({
                "indexes": event_idx[0]
            })
    
    with open(os.path.join(os.environ['HOME'], f"./.local/whow/events/{event_entry.name.replace(' ', '_')}.toml"), "w") as tml:
        event_entry_to = event_entry.event_to if event_entry.event_to is not None else EventDateTime()

        t = toml.dumps(
            {
                event_entry.name: {
                    "index": event_idx[1] if not use_old_index else event_entry.index,
                    "name": event_entry.name,
                    "event_from": event_entry.event_from.__repr__(),
                    "event_to": event_entry_to.__repr__(),
                    "description": event_entry.description,
                    "full_day": event_entry.full_day,
                    "categories": [c.name for c in event_entry.categories],
                }
            }
        )
        tml.write(t)
    
    return f"Registered New Event: \n{t}"

def parse_evententry_from_dict(d: dict[str, dict[str, str | bool | list[str | int]]], filename: str) -> EventEntry:
    """
    Parse a dictionary that was parsed from an `EventEntry` into an `EventEntry`.
    `file_name` should be the name of the file WITHOUT the extension
    """

    return EventEntry(
        str(d[filename]["name"]).replace("_", " "),
        get_eventdatetime_from_str(str(d[filename]["from"])),
        get_eventdatetime_from_str(str(d[filename]["to"])) if d[filename]["to"] != "None" else None,
        str(d[filename]["description"]),
        [parse_category_from_name(c) for c in d[filename]["categories"]], # type: ignore
        full_day=True if d[filename]["to"] != "None" else False
    )

def match_event_index(index: int) -> str:
    """
    Find an event filename based on its index.
    """

    BASEDIR = os.path.join(os.environ['HOME'], f"./.local/whow/events")

    for filename in os.listdir(BASEDIR):
        if filename == "index.toml":
            continue

        d = toml.load(os.path.join(BASEDIR, filename))
        if index == d[os.path.splitext(filename.replace("_", " "))[0]]["index"]:
            return filename
    
    raise IndexError("No file with this event index exists! Perhaps the index.toml is corrupted?")

def del_event(index: int) -> str:
    """
    Delete an event by its index.
    """

    try:
        filename = match_event_index(index)
    except IndexError:
        error("A to-do with this index does not exist! Please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""
    
    BASEDIR = os.path.join(os.environ['HOME'], f"./.local/whow/events")
    event_name = os.path.splitext(filename.replace("_", " "))[0]
    event = parse_evententry_from_dict(toml.load(os.path.join(BASEDIR, filename)), filename)

    if index == event.index:
        os.remove(os.path.join(BASEDIR, filename))
        pop_indextoml_element(index, type = "events")
        return f"deleted event: {event_name}"
    return "" 

def get_category_from_dict(d: dict) -> Category:
    return Category(
        d["name"],
        get_color_class_from_name(d["color"].lower())
    )

def list_categories() -> None:
    for path in os.path.join(os.environ['HOME'], "./.local/whow/categories"):
        try:
            print(get_category_from_dict(toml.load(os.path.join(os.environ['HOME'], "./.local/whow/categories", path))["name"]))
        except KeyError or TypeError:
            warn(f"The category file {path} in the folder is corrupted!")

# Development code
def debug_create_todo(name: str) -> ToDoEntry:
    category1 = Category("category1")
    category2 = Category("category2")
    return ToDoEntry(name, None, [category1, category2])

def debug_create_event(name: str) -> EventEntry:
    c1 = Category("category1")
    c2 = Category("category2")
    return EventEntry(name, EventDateTime(), None, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", [c1, c2], full_day=True)