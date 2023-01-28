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

import util

# Class Definitions
class Config():
    def __init__(self) -> None:
        self.default_separator:  str     = "line"
        self.enable_emojis:      bool    = True
        self.time_format:        int     = 12
        self.sections:           list    = [ "separator", "caldate", "separator", "important", "todos", "separator", "events", "separator", "schedule" ]


        self.CONFPATH = os.path.join(os.environ['HOME'], "./.config/whow/config.toml")
        if os.path.exists(self.CONFPATH):
            self.load_cfg()
        
    def load_cfg(self):
        data = toml.load(self.CONFPATH)

        self.default_separator = data['default_seperator']
        self.enable_emojis = data['enable_emojis']
        self.time_format = int(data['time_format'])
        self.sections = data['sections']

    def get_dict(self) -> dict[str, bool | str | int | list[str]]:
        return {
            "default_separator": self.default_separator,
            "enable_emojis": self.enable_emojis,
            "time_format": self.time_format,
            "sections": self.sections
        }
 
    def dump_cfg(self) -> None:
        toml.dump(self.get_dict(), os.path.join(os.environ['HOME'], "./.config/whow/config.toml"))
    
    def write_cfg(self, force: bool = False, quiet: bool = False) -> None:
        CONFPATH = os.path.join(os.environ['HOME'], "./.config/whow/config.toml")

        if os.path.exists(CONFPATH):
            if not force:
                util.warn("Configuration already exists. Aborting.") if not quiet else None
                return
            util.warn("Configuration already exists. Overwriting.") if not quiet else None

        toml.dump(self.get_dict(), CONFPATH)


# Function Definitions

