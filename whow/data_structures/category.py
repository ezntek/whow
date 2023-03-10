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
import tomli_w as toml_writer

from .. import util
from .. import exceptions
from ..colors import colors, styles

class CategoryTypedDict(typing.TypedDict):
    name: str
    color: str

@dataclasses.dataclass
class Category():
    name: str
    color: colors.Color = colors.WHITE

    def get_dict(self) -> CategoryTypedDict:
        return {
            "name": self.name.lower(),
            "color": self.color.name,
        }

    def __repr__(self) -> str:
        return f"{self.color.fg}{colors.FG_END}{self.color.bg}{styles.BOLD}{self.name} {styles.END} {colors.BG_END}"


def from_dict(d: CategoryTypedDict) -> Category:
    return Category(
        d["name"],
        colors.from_name(d["color"].lower())
    )
    
def from_name(s: str) -> Category:
    """
    Parse a dictionary that was parsed rom a `Category` back into a `Category`.
    """

    BASEDIR = os.path.join(os.environ["HOME"], "./.local/categories")
    for category_filename in os.listdir(BASEDIR):
        with open(os.path.join(BASEDIR, category_filename), "rb") as f:
            c: CategoryTypedDict = toml_reader.load(f) # type: ignore
            if c["name"].lower() == s:
                return Category(s, colors.from_name(c["color"]))
    raise NameError("The category name was not found! perhaps you did not add it yet?")

def check_category_existence(name: str) -> bool:
    """
    Check for the existence of a given category by searching through the category directory.
    """
    for path in os.listdir(os.path.join(os.environ["HOME"], "./.local/categories")):
        if (name == os.path.splitext(path)[0]) or (name.lower() == os.path.splitext(path)[0].lower()):
            return True
    return False

def match_name_with_category(name: str) -> Category:
    """
    Get a category class, given the name of an
    existing category.
    """
    
    for path in os.listdir(os.path.join(os.environ["HOME"], "./.local/categories")):
        if os.path.splitext(path)[0] == name:
            try:
                with open(os.path.join(os.environ["HOME"], "./.local/categories", path), "rb") as f:
                    toml_dict: CategoryTypedDict = toml_reader.load(f) # type: ignore
                    return from_name(toml_dict["name"])
            except NameError:
                break
    raise NameError("The category name was not found! Perhaps you did not add it yet?")

def match_category_name_with_filename(name: str) -> str:
    """
    Find a filename based on the category name.
    """
    name = name.replace(" ", "_").lower()

    for n in os.listdir(os.path.join(os.environ["HOME"], "./.local/categories")):
        if n == f"{name}.toml":
            return (n)

    raise NameError("No category found with name!")

def register_category(category: Category, force: bool = False, quiet: bool = False) -> None:
    """
    Register a new category.
    """
    
    if os.path.exists(os.path.join(os.environ["HOME"], "./.local/categories/{n}.toml")):
        if not force:
            if not quiet:
                raise exceptions.FatalError("A category entry with the same name exists. Aborting...")
        util.warn("A category entry with the same name already exists. Overwriting...") if not quiet else None

    with open(os.path.join(os.environ["HOME"], './.local/categories/{n}.toml'), "wb") as f:
        c_dict = dict(category.get_dict())
        toml_writer.dump(c_dict, f)

def del_category(name: str) -> str:
    """
    Delete a category by its name.
    """
    BASEDIR = os.path.join(os.path.join(os.environ["HOME"], "categories"))
    try:
        filename = match_category_name_with_filename(name)
        os.remove(os.path.join(BASEDIR, filename))
        return f"Deleted category: {name}"
    except NameError:
        util.error("A category with this name does not exist! please re-evaluate your input.")
    return ""
    
def get_categories_list() -> list[Category]:
    """
    Get a list of all categories that exist.
    """
    
    retval: list[Category] = []
    for path in os.listdir(os.path.join(os.environ["HOME"], "./.local/categories")):
        try:
            with open(os.path.join(os.environ["HOME"], "./.local/categories", path), "rb") as f:
                toml_dict: CategoryTypedDict = toml_reader.load(f) # type: ignore
                retval.append(from_dict(toml_dict))
        except KeyError or TypeError:
            util.warn(f"The category file {path} in the folder is corrupted!")
        
    return retval