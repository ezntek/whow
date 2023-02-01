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
from config import Config
from exceptions import *

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
def clean_empty_strings_in_list(l: list[str]) -> list[str]:
    for count, element in enumerate(l):
        l.pop(count) if element == "" else None
    return l

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

def emoji(emoji: str, cfg: Config = Config()) -> str | None:
    """
    Print out an emoji if `enable_emojis` is set to true on the configuration.
    """
    if cfg.enable_emojis:
        return emoji

def sfprint(string: str, padding: int = 0, flowtext: bool = True) -> str:
    """
    Return a string, omitting overflowed text based
    on the terminal width.
    """

    term_width = shutil.get_terminal_size().columns - 2 - padding
    overflow = '…' if flowtext and (len(string) + padding) > term_width else ''
    text_padding: str = " "*padding

    return(f"{text_padding}{string[0:term_width]}{overflow}")

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

def parse_category_from_name(s: str, cfg: Config) -> Category:
    """
    Parse a dictionary that was parsed from a `Category` back into a `Category`.
    """

    BASEDIR = os.path.join(cfg.data_tree_dir, "categories")
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
        overdue=True if (type(d[file_name]["overdue"]) == bool and d[file_name]["overdue"]) or (datetime.datetime.now().date() > due) else False,
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
    retval: list[int | str] = []
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

def pop_indextoml_element(element: int, cfg: Config, type: str = "todos",) -> None:
    """
    Remove an entry from an index.toml.
    Valid values for `type: str` include `"todos"` and `"events"`.
    """

    if type != "todos" and type != "events":
        type = "todos"
    
    with open(os.path.join(cfg.data_tree_dir, f"todos/index.toml"), "r") as index_toml:
        indexes: list[int | str] = toml.loads(index_toml.read())['indexes']
        for count, idx in enumerate(indexes):
            if idx == element:
                indexes[count] = "None"
    
    with open(os.path.join(cfg.data_tree_dir, f"todos/index.toml"), "w") as index_toml:
        index_toml.write(toml.dumps({
            "indexes": indexes
        }))

def match_todo_index(index: int, cfg: Config) -> str:
    """
    Find a to-do filename based on its index.
    """

    BASEDIR = os.path.join((cfg.data_tree_dir), f"todos")
    for filename in os.listdir(BASEDIR):
        if filename == "index.toml":
            continue
        data = toml.load(os.path.join(BASEDIR, filename))
        todo_name = os.path.splitext(filename.replace("_", " "))[0]

        if index == data[todo_name]["index"]:
            return filename
    raise IndexError('No file with this to-do index exists! Perhaps the index.toml is corrupted?')

def del_todo(index: int, cfg: Config) -> str:
    """
    Delete a to-do by its index.
    """
    
    try:
        filename = match_todo_index(index, cfg)
    except IndexError:
        error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""
        
    BASEDIR = os.path.join((cfg.data_tree_dir), f"todos")
    todo_name = os.path.splitext(filename.replace("_", " "))[0]
    todo = parse_todoentry_from_dict(toml.load(os.path.join(BASEDIR, filename)), os.path.splitext(filename)[0].replace("_", " "))
    
    if index == todo.index:
        os.remove(os.path.join(BASEDIR, filename))
        pop_indextoml_element(index, cfg)
        return f"Deleted to-do: {todo_name}\n"
    return ""

def mark_todo(index: int, cfg: Config) -> str:
    """
    Tick a to-do as done/undone.
    """

    try:
        filename = match_todo_index(index, cfg)
    except IndexError:
        error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""

    data = toml.load(os.path.join((cfg.data_tree_dir), f'todos', filename))
    todo_name = os.path.splitext(filename.replace("_", " "))[0]
    todo = parse_todoentry_from_dict(data, todo_name)
    
    todo.ticked = not todo.ticked
    register_todo(todo, cfg, force=True, quiet=True, use_old_index=True)
    
    return f"Marked to-do: {filename} as {not todo.ticked}\n" 

def unify_date_formats(string: str) -> str:
    # The time format stays uniform, whereas
    # there are multiple supported date formats,
    # such as:
    #
    # dd/mm/YYYY
    # YYYY/mm/dd
    # MTH dd YYYY (e.g. Jan 09 2069) or MTH dd, YYYY
    
    CONVERSION_TABLE = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12
    }

    whitespace_split_string = string.split(" ")
    if len(whitespace_split_string) == 3:
        for k, v in CONVERSION_TABLE.items():
            if whitespace_split_string[0].lower() == k:
                return f"{whitespace_split_string[1].replace(',', '')}/{str(v)}/{whitespace_split_string[2]}"
        return ""
    if len(whitespace_split_string) == 2:
        if "," in whitespace_split_string[1]: # "MTH dd,YYYY"
            tmp = whitespace_split_string[1].split(',') # ["dd", 'YYYY"]
            try:
                return f"{tmp[0]}/{CONVERSION_TABLE[whitespace_split_string[0].lower()]}/{tmp[1]}"
            except KeyError:
                raise InvalidMonthNameError()
    del whitespace_split_string

    try:
        split_string = [int(val) for val in string.split("/")]
    except ValueError:
        raise DateFormattingError()
    if split_string[0] > 99:
        return f"{split_string[2]}/{split_string[1]}/{split_string[0]}"
    elif split_string[2] > 99:
        return string

    raise DateFormattingError()

def parse_argv_event_datetime(string: str) -> EventDateTime:
    # either:
    #   "mm/dd/YYYY 6:09:34 PM" | "mm/dd/YYYY 6:09PM"
    # or:
    #   "mm/dd/YYYY 18:09:34"
    #
    # where seconds can be omitted.
    
    twelve_hour_time: bool = True if "PM" or "AM" in string else False
    afternoon_time: bool = False
    
    s1 = clean_empty_strings_in_list(string.split(" ")) # ["mm/dd/YYYY", "6:09", "PM"] or ["mm/dd/YYYY", "6:09PM"]
    if len(s1) == 3 and s1[-1].lower() == "pm":
        afternoon_time = True
        s1.pop(2) # ["mm/dd/YYYY", "6:09"]
        
    if len(s1) == 2 and s1[-1][-2:].lower() == "pm":
        afternoon_time = True
        s1[-1] = s1[-1][:-2] # ["mm/dd/YYYY", "6:09PM"] -> ["mm/dd/YYYY", "6:09"]
    
    # len(s1) should be 2 by now

    date_part_list = unify_date_formats(s1[0]).split("/")
    time_part_list = s1[1].split(":")

    if twelve_hour_time:
        time_part_list[0] = str(int(time_part_list[0]) + 12) if afternoon_time else time_part_list[0]

    date_part = datetime.date(int(date_part_list[2]), int(date_part_list[1]), int(date_part_list[0]))
    time_part = datetime.time(int(time_part_list[0]), int(time_part_list[1]), int(time_part_list[2])) if len(time_part_list) == 3 else datetime.time(int(time_part_list[0]), int(time_part_list[1]), 0)

    return EventDateTime(date_part, time_part)

def register_todo(todo_entry: ToDoEntry, cfg: Config, force: bool = False, quiet: bool = False, use_old_index: bool = False) -> str | None:
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
    #todo_entry.name.replace(" ", "_")

    # guard clause
    if os.path.exists(os.path.join(cfg.data_tree_dir, f"todos/{todo_entry.name}.toml")):
        if not force:
            warn("A to-do entry with the same name exists. Aborting.") if not quiet else None
            return
        warn("A to-do entry with the same name already exists. Overwriting.") if not quiet else None

    todo_idx = (0, 0)
    if not use_old_index:
        # load the used indexes
        with open(os.path.join(cfg.data_tree_dir, "todos/index.toml")) as indexes:
            idx: list[int | str] = toml.loads(indexes.read())['indexes']
        
        todo_idx = _fill_idx(idx)

        # write new index.toml
        with open(os.path.join(cfg.data_tree_dir, "todos/index.toml"), "w") as indextoml:
            indextoml.write(toml.dumps({
                "indexes": todo_idx[0]
            }))

    # write the todo toml file
    with open(os.path.join(cfg.data_tree_dir, f'todos/{todo_entry.name.replace(" ", "_")}.toml'), "w+") as tml:
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

def init(destroy: bool = False, verbose: bool = False) -> None:
    """
    Create the necessary paths for the To-Dos and Events.
    """
    cfg = Config() # no existing config exists yet
    
    log("Reconfiguring Whow...") if verbose else None

    if destroy:
        warn(f"Overwriting {cfg.config_tree_dir} and {cfg.data_tree_dir}...")
        try:
            shutil.rmtree(cfg.config_tree_dir)
            shutil.rmtree(cfg.data_tree_dir)
        except FileNotFoundError:
            pass

    # create dirs
    dirs = [
        cfg.data_tree_dir,
        os.path.join(os.environ['HOME'], "./.config/whow")
    ]

    tree_dirs = [
            "todos",
            "categories",
            "events",
    ]

    for dir in dirs:
        if not os.path.isdir(dir):
            log(f"Created directory {dir}.") if verbose else None
            os.mkdir(dir)

    for dir in tree_dirs:
        if not os.path.isdir(os.path.join(cfg.data_tree_dir, dir)):
            log(f"Created directory {dir}.") if verbose else None
            os.mkdir(os.path.join(cfg.data_tree_dir, dir))
    

    indextoml_tmp = toml.dumps(
        {
            "indexes": [] # type: ignore
        }
    )

    # write the index.toml's
    todos_indextoml = open(os.path.join(cfg.data_tree_dir, 'todos/index.toml'), "w+")
    events_indextoml = open(os.path.join(cfg.data_tree_dir, 'events/index.toml'), "w+") 
    todos_indextoml.write(indextoml_tmp)
    events_indextoml.write(indextoml_tmp)

    todos_indextoml.close()
    events_indextoml.close()

    # create the default config.toml
    log("Writing configuration file...") if verbose else None
    cfg.write_cfg(quiet=True)
    
    # create a new important category
    log("Registering important category...") if verbose else None
    register_category(Category("important", Colors.red()), cfg, force=True)

def split_string_date(string_date: str) -> datetime.date:
    """
    Split a string date in the date/month/year format into a datetime.date object.
    """
    string_date_array = string_date.split("/")

    if not string_date:
        return datetime.date(1, 1, 1)

    if (int(string_date_array[0]) > 31) or (int(string_date_array[1]) > 12):
        error("The date you supplied was invalid! It has to follow the date/month/year format.")
        exit()
    
    return datetime.date(int(string_date_array[2]), int(string_date_array[1]), int(string_date_array[0]))

def check_category_existence(name: str, cfg: Config) -> bool:
    """
    Check for the existence of a given category by searching through the category directory.
    """
    for path in os.listdir(os.path.join(cfg.data_tree_dir, f"categories")):
        if (name == os.path.splitext(path)[0]) or (name.lower() == os.path.splitext(path)[0].lower()):
            return True
    return False

def match_name_with_category(name: str, cfg: Config) -> Category:
    """
    Get a category class, givven the name of an
    existing category.
    """
    
    for path in os.listdir(os.path.join(cfg.data_tree_dir, f"categories")):
        if os.path.splitext(path)[0] == name:
            try:
                return parse_category_from_name(toml.load(os.path.join(cfg.data_tree_dir, "categories", path))['name'], cfg)# type: ignore
            except NameError:
                break
    raise NameError("The category name was not found! Perhaps you did not add it yet?")

def match_category_name_with_filename(name: str, cfg: Config) -> str:
    """
    Find a filename based on the category name.
    """
    name = name.replace(" ", "_").lower()

    for n in os.listdir(os.path.join(cfg.data_tree_dir, f"categories")):
        if n == f"{name}.toml":
            return(n)

    raise NameError("No category found with name!")

def register_category(category: Category, cfg: Config, force: bool = False, quiet: bool = False) -> str | None:
    """
    Register a new category.
    """
    
    n = category.name.replace(" ", "_")

    if os.path.exists(os.path.join(cfg.data_tree_dir, f"categories/{n}.toml")):
        if not force:
            warn("A category entry with the same name exists. Aborting...") if not quiet else None
            return
        warn("A category entry with the same name already exists. Overwriting...") if not quiet else None

    with open(os.path.join(cfg.data_tree_dir, f'categories/{n}.toml'), "w+") as categorytoml:
        t = toml.dumps(category.get_dictionary())
        categorytoml.write(t)

    return f"Wrote a new category toml. \n{t}" if not quiet else None


def del_category(name: str, cfg: Config) -> str:
    """
    Delete a category by its name.
    """
    BASEDIR = os.path.join(os.path.join(cfg.data_tree_dir, f"categories"))
    try:
        filename = match_category_name_with_filename(name, cfg)
        os.remove(os.path.join(BASEDIR, filename))
        return f"Deleted category: {name}"
    except NameError:
        error("A category with this name does not exist! please re-evaluate your input.")
    return ""

def register_event(event_entry: EventEntry, cfg: Config, force: bool = False, quiet: bool = False) -> str:
    """
    Register a new event.  

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
    """

    event_entry.name.replace(" ", "_")

    if os.path.exists(os.path.join(cfg.data_tree_dir, f"{event_entry.name}.toml")):
        if not force:
            warn("An event entry with the same name exists, aborting.") if not quiet else None
            return ""
        warn("An event entry with the same name already exists. Overwriting.") if not quiet else None
        
    event_idx = _fill_idx(toml.load(os.path.join(cfg.data_tree_dir, "index.toml"))['indexes'])
    with open(os.path.join(cfg.data_tree_dir, "events/index.toml"), "w") as indextoml:
        indextoml.write(toml.dumps({"indexes": event_idx[0]}))
    
    with open(os.path.join(cfg.data_tree_dir, f"events/{event_entry.name.replace(' ', '_')}.toml"), "w") as tml:
        event_entry_to = event_entry.event_to if event_entry.event_to is not None else "fullday"

        t = toml.dumps(
            {
                event_entry.name: {
                    "index": event_idx[1],
                    "name": event_entry.name,
                    "event_from": event_entry.event_from.__repr__(),
                    "event_to": event_entry_to.__repr__() if type(event_entry_to) != str else event_entry_to,
                    "description": event_entry.description,
                    "full_day": event_entry.full_day,
                    "categories": [c.name for c in event_entry.categories],
                }
            }
        )
        tml.write(t)
    
    return f"Registered New Event: \n{t}"

def parse_evententry_from_dict(d: dict[str, dict[str, str | bool | list[str | int]]], file_name: str) -> EventEntry:
    """
    Parse a dictionary that was parsed from an `EventEntry` into an `EventEntry`.
    `file_name` should be the name of the file WITHOUT the extension
    """

    return EventEntry(
        str(d[file_name]["name"]).replace(" ", "_"),
        parse_argv_event_datetime(str(d[file_name]["event_from"])),
        parse_argv_event_datetime(str(d[file_name]["event_to"])) if d[file_name]["event_to"] != "None" else None,
        str(d[file_name]["description"]),
        [parse_category_from_name(c) for c in d[file_name]["categories"]], # type: ignore
        full_day=True if d[file_name]["event_to"] != "None" else False
    )

def match_event_index(index: int, cfg: Config) -> str:
    """
    Find an event filename based on its index.
    """

    BASEDIR = os.path.join(cfg.data_tree_dir, f"events")

    for filename in os.listdir(BASEDIR):
        if filename == "index.toml":
            continue

        d = toml.load(os.path.join(BASEDIR, filename))
        if index == d[os.path.splitext(filename.replace("_", " "))[0]]["index"]:
            return filename
    
    raise IndexError("No file with this event index exists! Perhaps the index.toml is corrupted?")

def del_event(index: int, cfg: Config) -> str:
    """
    Delete an event by its index.
    """

    try:
        filename = match_event_index(index, cfg)
    except IndexError:
        error("An event with this index does not exist! Please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""
    
    BASEDIR = os.path.join(cfg.data_tree_dir, f"events")
    event_name = os.path.splitext(filename.replace("_", " "))[0]
    event = parse_evententry_from_dict(toml.load(os.path.join(BASEDIR, filename)), os.path.splitext(filename)[0].replace("_", " "))

    if index == event.index:
        os.remove(os.path.join(BASEDIR, filename))
        pop_indextoml_element(index, cfg, type = "events")
        return f"deleted event: {event_name}"
    return "" 

def parse_category_from_dict(d: dict[str, str]) -> Category:
    """
    Parse a category that was parsed from a `Category` into a `Category`.
    """
    return Category(
        d["name"],
        get_color_class_from_name(d["color"].lower())
    )

def list_categories(cfg: Config) -> None:
    """
    List all categories.
    """
    
    for path in os.listdir(os.path.join(cfg.data_tree_dir, "categories")):
        try:
            print(parse_category_from_dict(toml.load(os.path.join(cfg.data_tree_dir, "categories", path))))
        except KeyError or TypeError:
            warn(f"The category file {path} in the folder is corrupted!")