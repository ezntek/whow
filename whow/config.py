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

# Imports
import toml
import os
import colors

# Class Definitions

class Config():
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
        data = toml.load(self.CONFPATH)

        self.default_separator:str = data['config']['default_separator'] if "default_separator" in data['config'].keys() else self.default_separator
        self.separator_length: int = data['config']['separator_length'] if "separator_length" in data['config'].keys() else self.separator_length
        self.enable_emojis: bool = data['config']['enable_emojis'] if "enable_emojis" in data['config'].keys() else self.enable_emojis
        self.time_format: int = int(data['config']['time_format']) if "time_format" in data['config'].keys() else self.time_format
        self.config_tree_dir: str = data['config']['config_tree_dir'].format(HOME=os.environ['HOME']) if "config_tree_dir" in data['config'].keys() else self.config_tree_dir
        self.sections: list[str] = data['config']['sections'] if "sections" in data['config'].keys() else self.sections

    def get_dict(self) -> dict[str, dict[str, bool | str | int | list[str]]]:
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
                print(f"{colors.Styles.bold}{colors.Colors.magenta().colorprint('[!!]')}{colors.Styles.end}Configuration already exists. Aborting.") if not quiet else None
                return
            print(f"{colors.Styles.bold}{colors.Colors.magenta().colorprint('[!!]')}{colors.Styles.end}Configuration already exists. Overwriting.") if not quiet else None
        with open(CONFPATH, "w") as conffile:
            toml.dump(self.get_dict(), conffile) # type: ignore