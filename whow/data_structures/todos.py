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

class ToDoTypedDict(typing.TypedDict):
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

    def to_dict(self) -> ToDoTypedDict:
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
    def from_dict(d: ToDoTypedDict):
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

def pop_indextoml_element(element: int, type: str = "todos",) -> None:
    """
    Remove an entry from an index.toml.
    Valid values for `type: str` include `"todos"` and `"events"`.
    """

    if type != "todos" and type != "events":
        type = "todos"
    
    with open(os.path.join(os.environ["HOME"], "./.local/todos/index.toml"), "r") as index_toml:
        indexes: list[int] = toml_reader.loads(index_toml.read())['indexes']
        for count, idx in enumerate(indexes):
            if idx == element:
                indexes[count] = -1
    
    with open(os.path.join(os.environ["HOME"], "./.local/todos/index.toml"), "w") as index_toml:
        index_toml.write(toml_writer.dumps({
            "indexes": indexes
        }))

def match_todo_index(index: int) -> str:
    """
    Find a to-do filename based on its index.
    """

    BASEDIR = os.path.join(os.environ["HOME"], "./.local/todos")
    for filename in os.listdir(BASEDIR):
        if filename == "index.toml":
            continue
        with open(os.path.join(BASEDIR, filename), "rb") as f:
            data = toml_reader.load(f)
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
        util.error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""
        
    BASEDIR = os.path.join(os.environ["HOME"], "./.local/todos")
    todo_name = os.path.splitext(filename.replace("_", " "))[0]
    with open(os.path.join(BASEDIR, filename), "rb") as f:
        todo: ToDoEntry = ToDoEntry.from_dict(toml_reader.load(f)) # type: ignore
    
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
        util.error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""

    with open(os.path.join(os.environ["HOME"], f'./.local/todos/{filename}'), "rb") as f:
        data = toml_reader.load(f)

    todo = ToDoEntry.from_dict(data)
    
    todo.ticked = not todo.ticked
    register_todo(todo, force=True, quiet=True)
    
    return f"Marked to-do: {filename} as {not todo.ticked}\n" 

def register_todo(todo_entry: ToDoEntry, force: bool = False, quiet: bool = False) -> typing.Union[str, None]:
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
        todos_tree: dict[str, dict[str, ToDoTypedDict]] = toml_reader.load(f) # type: ignore

    # guard clause
    if todo_entry.name in todos_tree.keys():
        if not force:
            if not quiet:
                raise exceptions.FatalError("A to-do entry with the same name exists. Aborting.")
        elif force:
            util.warn("A to-do entry with the same name already exists. Overwriting.") if not quiet else None

    todo_entry_dict = todo_entry.to_dict()
    t: str = toml_writer.dumps(todo_entry_dict)
    
    todos_tree["todos"][todo_entry.name] = todo_entry_dict

    return f"Registered New To-Do: \n{t}"
