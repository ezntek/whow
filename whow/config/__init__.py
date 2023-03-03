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

# Imports
import os
import typing

from ..colors import colors, styles

try:
    import tomllib as toml_reader
except ImportError:
    import tomli as toml_reader

# Class Definitions
class _Singleton():
    _instance = None
    def __new__(cls, *args: typing.Any, **kwargs: typing.Any):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class Config(_Singleton):
    def __init__(self, 
                default_separator:  str       = "line",
                separator_length:   int       = 27,
                enable_emojis:      bool      = True,
                time_format:        int       = 12,
                data_tree_dir:      str       = os.path.join(os.environ['HOME'], "./.local/whow"),
                config_tree_dir:    str       = os.path.join(os.environ['HOME'], "./.config/whow"),
                sections:           list[str] = [ "separator", "datetime", "separator", "calendar", "separator", "todos", "separator", "events"]) -> None:
        "Create a new config instance."

        self.default_separator: str = default_separator
        self.separator_length: int = separator_length
        self.enable_emojis: bool = enable_emojis
        self.time_format: int = time_format
        self.config_tree_dir: str = config_tree_dir
        self.sections: list[str] = sections
        self.data_tree_dir: str = data_tree_dir

        self.CONFPATH = os.path.join(os.environ['HOME'], "./.config/whow/config.toml")
        if os.path.exists(self.CONFPATH):
            self.load_cfg()
            
    def load_cfg(self):
        """
        Load configuration file. Shouldn't be called on its own.
        """
        with open(self.CONFPATH, "rb") as f:
            data = toml_reader.load(f)

        self.default_separator:str = data['config']['default_separator'] if "default_separator" in data['config'].keys() else self.default_separator
        self.separator_length: int = data['config']['separator_length'] if "separator_length" in data['config'].keys() else self.separator_length
        self.enable_emojis: bool = data['config']['enable_emojis'] if "enable_emojis" in data['config'].keys() else self.enable_emojis
        self.time_format: int = int(data['config']['time_format']) if "time_format" in data['config'].keys() else self.time_format
        self.config_tree_dir: str = data['config']['config_tree_dir'].format(HOME=os.environ['HOME']) if "config_tree_dir" in data['config'].keys() else self.config_tree_dir
        self.sections: list[str] = data['config']['sections'] if "sections" in data['config'].keys() else self.sections

    def get_dict(self) -> dict[str, dict[str, typing.Union[bool, str, int, list[str]]]]:
        """
        Return a dictionary of current configuration values.
        """
        return {
            "config": {
                "default_separator": self.default_separator,
                "separator_length": self.separator_length,
                "enable_emojis": self.enable_emojis,
                "time_format": self.time_format,
                "config_tree_dir": self.config_tree_dir,
                "data_tree_dir": self.data_tree_dir,
                "sections": self.sections
            }
        }
 
    def write_cfg(self, force: bool = False, quiet: bool = False) -> None:
        """
        Write a new configuration if current configuration does not exist.
        """
        CONFPATH = os.path.join(os.environ['HOME'], "./.config/whow/config.toml")

        if os.path.exists(CONFPATH):
            if not force:
                print(f"{styles.BOLD}{colors.MAGENTA.sprint('[!!]')}{styles.END}Configuration already exists. Aborting.") if not quiet else None
                return
            print(f"{styles.BOLD}{colors.MAGENTA.sprint('[!!]')}{styles.END}Configuration already exists. Overwriting.") if not quiet else None
        with open(CONFPATH, "w") as conffile:
            toml.dump(self.get_dict(), conffile) # type: ignore

    def nuke_cfg(self) -> None:
        "Nuke the configuration file. Highly destructive."
        os.remove(os.path.join(self.config_tree_dir, "config.toml"))