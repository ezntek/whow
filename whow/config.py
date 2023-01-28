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
                seperator_length:   int       = 27,
                enable_emojis:      bool      = True,
                time_format:        int       = 12,
                sections:           list[str] = [ "separator", "caldate", "separator", "important", "todos", "separator", "events", "separator", "schedule" ]) -> None:
        "Create a new config instance."
        
        self.default_separator = default_separator
        self.seperator_length = seperator_length
        self.enable_emojis = enable_emojis
        self.time_format = time_format
        self.sections = sections

        self.CONFPATH = os.path.join(os.environ['HOME'], "./.config/whow/config.toml")
        if os.path.exists(self.CONFPATH):
            self.load_cfg()
            
    def load_cfg(self) -> None:
        data = toml.load(self.CONFPATH)

        self.default_separator = data['config']['default_separator'] if "default_seperator" in data.keys() else self.default_separator
        self.seperator_length = data['config']['separator_length'] if "separator_length" in data.keys() else self.seperator_length
        self.enable_emojis = data['config']['enable_emojis'] if "enable_emojis" in data.keys() else self.enable_emojis
        self.time_format = int(data['config']['time_format']) if "time_format" in data.keys() else self.time_format
        self.sections = data['config']['sections'] if "sections" in data.keys() else self.sections
        

    def get_dict(self) -> dict[str, dict[str, bool | str | int | list[str]]]:
        return {
            "config": {
                "default_separator": self.default_separator,
                "separator_length": self.seperator_length,
                "enable_emojis": self.enable_emojis,
                "time_format": self.time_format,
                "sections": self.sections
            }
        }
 
    def write_cfg(self, force: bool = False, quiet: bool = False) -> None:
        CONFPATH = os.path.join(os.environ['HOME'], "./.config/whow/config.toml")

        if os.path.exists(CONFPATH):
            if not force:
                print(f"{colors.Styles.bold}{colors.Colors.magenta().colorprint('[!!]')}{colors.Styles.end}Configuration already exists. Aborting.") if not quiet else None
                return
            print(f"{colors.Styles.bold}{colors.Colors.magenta().colorprint('[!!]')}{colors.Styles.end}Configuration already exists. Overwriting.") if not quiet else None
        toml.dump(self.get_dict(), CONFPATH) # type: ignore


# Function Definitions

