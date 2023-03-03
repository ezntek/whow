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
    config,
    exceptions,
    util
)

class ToDoTypedDict(typing.TypedDict):
    index: int
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

    def to_dict(self, index: int, use_old_index: bool) -> dict[str, ToDoTypedDict]:
        todo_entry_due = self.due if self.due is not None else datetime.datetime.now().date()

        return {
            self.name: {
                "index": index if not use_old_index else self.index,
                "name": self.name,
                "due": todo_entry_due
                       if self.due is not None else
                       datetime.datetime.now().date(),
                "categories": [c.name for c in self.categories],
                "overdue": False if datetime.datetime.now().date() < todo_entry_due else True,
                "ticked": self.ticked
            }
        }

    @staticmethod
    def from_dict(d: dict[str, ToDoTypedDict], file_name: str):
        """
        Parse a dictionary that was parsed from a `ToDoEntry` into a `ToDoEntry`.
        `file_name` should be the name of the file WITHOUT the extension.
        """
        return ToDoEntry(
            d[file_name]["name"].replace("_", " "),
            d[file_name]["due"],
            [category.from_name(c) for c in d[file_name]["categories"]],
            overdue=True if (type(d[file_name]["overdue"]) == bool and d[file_name]["overdue"]) or (datetime.datetime.now().date() > d[file_name]["due"]) else False,
            ticked=d[file_name]["ticked"],
            index=d[file_name]["index"]
        )

def _fill_idx(l: list[int]) -> tuple[list[int], int]:
    """
    fill an index.toml indexes list.
    This function is to bypass the use
    of a for-else clause, which is
    deprecated.
    """
    
    retval: list[int] = []
    idx = 0
    found_spot = False

    for count, i in enumerate(l):
        retval.append(count)
        if i == -1:
            found_spot = True
            idx = count
    
    if not found_spot:
        retval.append(len(retval))
        idx = len(retval) - 1
     
    return (retval, idx)

def pop_indextoml_element(element: int, cfg: config.Config = config.Config(), type: str = "todos",) -> None:
    """
    Remove an entry from an index.toml.
    Valid values for `type: str` include `"todos"` and `"events"`.
    """

    if type != "todos" and type != "events":
        type = "todos"
    
    with open(os.path.join(cfg.data_tree_dir, f"todos/index.toml"), "r") as index_toml:
        indexes: list[int] = toml_reader.loads(index_toml.read())['indexes']
        for count, idx in enumerate(indexes):
            if idx == element:
                indexes[count] = -1
    
    with open(os.path.join(cfg.data_tree_dir, f"todos/index.toml"), "w") as index_toml:
        index_toml.write(toml_writer.dumps({
            "indexes": indexes
        }))

def match_todo_index(index: int, cfg: config.Config = config.Config()) -> str:
    """
    Find a to-do filename based on its index.
    """

    BASEDIR = os.path.join((cfg.data_tree_dir), f"todos")
    for filename in os.listdir(BASEDIR):
        if filename == "index.toml":
            continue
        with open(os.path.join(BASEDIR, filename), "rb") as f:
            data = toml_reader.load(f)
        todo_name = os.path.splitext(filename.replace("_", " "))[0]

        if index == data[todo_name]["index"]:
            return filename
    raise IndexError('No file with this to-do index exists! Perhaps the index.toml is corrupted?')

def del_todo(index: int, cfg: config.Config = config.Config()) -> str:
    """
    Delete a to-do by its index.
    """
    
    try:
        filename = match_todo_index(index, cfg)
    except IndexError:
        util.error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""
        
    BASEDIR = os.path.join((cfg.data_tree_dir), f"todos")
    todo_name = os.path.splitext(filename.replace("_", " "))[0]
    with open(os.path.join(BASEDIR, filename), "rb") as f:
        todo = ToDoEntry.from_dict(toml_reader.load(f), os.path.splitext(filename)[0].replace("_", " "))
    
    if index == todo.index:
        os.remove(os.path.join(BASEDIR, filename))
        pop_indextoml_element(index, cfg)
        return f"Deleted to-do: {todo_name}\n"
    return ""

def mark_todo(index: int, cfg: config.Config = config.Config()) -> str:
    """
    Tick a to-do as done/undone.
    """

    try:
        filename = match_todo_index(index, cfg)
    except IndexError:
        util.error("A to-do with this index does not exist! please re-evaluate your input, or perhaps the index.toml is corrupted?")
        return ""

    with open(os.path.join((cfg.data_tree_dir), 'todos', filename), "rb") as f:
        data = toml_reader.load(f)

    todo_name = os.path.splitext(filename.replace("_", " "))[0]
    todo = ToDoEntry.from_dict(data, todo_name)
    
    todo.ticked = not todo.ticked
    register_todo(todo, cfg, force=True, quiet=True, use_old_index=True)
    
    return f"Marked to-do: {filename} as {not todo.ticked}\n" 

def register_todo(todo_entry: ToDoEntry, cfg: config.Config = config.Config(), force: bool = False, quiet: bool = False, use_old_index: bool = False) -> typing.Union[str, None]:
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

    if todo_entry.name == "index":
        raise exceptions.FatalError(f"invalid todo entry name: {todo_entry.name}")

    # replace all whitespaces with underscores
    todo_entry.name.replace(" ", "_")

    # guard clause
    if os.path.exists(os.path.join(cfg.data_tree_dir, f"todos/{todo_entry.name}.toml")):
        if not force:
            util.warn("A to-do entry with the same name exists. Aborting.") if not quiet else None
            return
        util.warn("A to-do entry with the same name already exists. Overwriting.") if not quiet else None
    
    if todo_entry.name == "index":
        util.warn(f"Illegal name: {todo_entry.name}")

    todo_idx = (0, 0)
    if not use_old_index:
        # load the used indexes
        with open(os.path.join(cfg.data_tree_dir, "todos/index.toml"), "rb") as f:
            idx: list[int] = toml_reader.load(f)['indexes']
        
        todo_idx = _fill_idx(idx)

        # write new index.toml
        with open(os.path.join(cfg.data_tree_dir, "todos/index.toml"), "w") as indextoml:
            indextoml.write(toml_writer.dumps({
                "indexes": todo_idx[0]
            }))

    # write the todo toml file
    with open(os.path.join(cfg.data_tree_dir, f'todos/{todo_entry.name.replace(" ", "_")}.toml'), "w+") as f:
        t = toml_writer.dumps(
            todo_entry.to_dict(todo_idx[1], use_old_index)
        )
        f.write(t)

    return f"Registered New To-Do: \n{t}"
