#    Copyright 2023 ezntek (ezntek@xflymusic.com) and DaringCuteSeal (daringcuteseal@gmail.com)
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
    
#      http://www.apache.org/licenses/LICENSE-2.0
    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import dataclasses
import typing
import datetime

try:
    import tomllib as toml_reader
except:
    import tomli as toml_reader

import tomli_w as toml_writer

from . import category
from .. import (
    exceptions,
    util
)

class ToDoEntryTypedDict(typing.TypedDict):
    name: str
    due: datetime.date
    categories: list[str]
    overdue: bool
    ticked: bool

@dataclasses.dataclass
class ToDoEntry():
    name: str
    due: datetime.date | None
    categories: list[category.Category]
    overdue: bool = False
    ticked: bool = False
    index: int = 0

    def to_dict(self) -> ToDoEntryTypedDict:
        todo_entry_due = self.due if self.due is not None else datetime.datetime.now().date()

        return {
            "name": self.name,
            "due": todo_entry_due
                   if self.due is not None else
                   datetime.datetime.now().date(),
            "categories": [c.name for c in self.categories],
            "overdue": False if datetime.datetime.now().date() < todo_entry_due else True,
            "ticked": self.ticked
        }
        

    @staticmethod
    def from_dict(d: ToDoEntryTypedDict):
        """
        Parse a dictionary that was parsed from a `ToDoEntry` into a `ToDoEntry`.
        `file_name` should be the name of the file WITHOUT the extension.
        """
        return ToDoEntry(
            d["name"].replace("_", " "),
            d["due"],
            [category.from_name(c) for c in d["categories"]],
            overdue=True if d["overdue"] or (datetime.datetime.now().date() > d["due"]) else False,
            ticked=d["ticked"],
        )

def match_todo_index(index: int) -> str:
    """
    Find a to-do name based on its index.
    """

    with open(os.path.join(os.environ["HOME"], "./.local/todos.toml"), "rb") as f:
        todos_tree: dict[str, ToDoEntryTypedDict] = toml_reader.load(f)

    for i, (_, v) in enumerate(todos_tree.items()):
        if i == index:
            return v["name"]
    
    raise exceptions.ToDoIndexError 

def unwrap_name_or_index(name_or_index: int | str) -> str:
    """
    Unrwap an index of a todo or the name of a todo into the todo, raising an exception if an error occurs.
    """    

    if isinstance(name_or_index, int):
        return match_todo_index(name_or_index)            
    elif type(name_or_index) is str:
        return name_or_index
    
    raise exceptions.NameOrIndexUnwrappingError

def del_todo(name_or_index: int | str) -> str:
    """
    Delete a to-do.
    """
    name = unwrap_name_or_index(name_or_index)

    with open(os.path.join(os.environ["HOME"], "./.local/todos.toml"), "rb") as f:
        todos_tree: dict[str, dict[str, ToDoEntryTypedDict]] = toml_reader.load(f)
    
    try:
        todos_tree["todos"].pop(name)
    except KeyError:
        raise exceptions.FatalError(f"The name {name} does not exist! Please re-evaluate your input.")

    with open(os.path.join(os.environ["HOME"], "./.local/todos.toml"), "rb") as f:
        toml_writer.dump(todos_tree, f)
    
    return f"Deleted To-Do {name}."
    
def mark_todo(name_or_index: int | str) -> str:
    """
    Tick a to-do as done/undone.
    """
    
    name = unwrap_name_or_index(name_or_index)
    with open(os.path.join(os.environ["HOME"], "./.local/todos.toml"), "rb") as f:
        todos_tree: dict[str, dict[str, ToDoEntryTypedDict]] = toml_reader.load(f)
    
    todo = ToDoEntry.from_dict(todos_tree["todos"][name])
    todo.ticked = not todo.ticked

    register_todo(todo, quiet=True, force=True)

    return f"Marked todo {name} as {todo.ticked}"

def register_todo(todo_entry: ToDoEntry, force: bool = False, quiet: bool = False) -> str | None:
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
    """
    
    # replace all whitespaces with underscores
    todo_entry.name.replace(" ", "_")

    # load todos
    with open(os.path.join(os.environ["HOME"], "./.local/todos.toml"), "rb") as f:
        todos_tree: dict[str, dict[str, ToDoEntryTypedDict]] = toml_reader.load(f) # type: ignore

    # guard clause
    if todo_entry.name in todos_tree.keys():
        if not force:
            if not quiet:
                raise exceptions.FatalError("A to-do entry with the same name exists. Aborting.")
        elif force:
            util.warn("A to-do entry with the same name already exists. Overwriting.") if not quiet else None

    todo_entry_dict: ToDoEntryTypedDict = todo_entry.to_dict()
    t: str = toml_writer.dumps(dict(todo_entry_dict))
    
    todos_tree["todos"][todo_entry.name] = todo_entry_dict

    with open(os.path.join(os.environ["HOME"], "./.local/todos.toml"), "wb") as f:
        toml_writer.dump(todos_tree, f)

    return f"Registered New To-Do: \n{t}"
