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

from dataclasses import dataclass
from util import Category

# Class Definitions

@dataclass
class ToDoEntry():
    name: str
    due: str | None
    categories: list[Category]
    overdue: bool = False

    def get_dictionary(self) -> dict[str, str | list[str | None]]:
        due = self.due if self.due is not None else 'N.A.'
        return {
            "name": self.name,
            "due": due,
            "categories": [c.name for c in self.categories],
            "overdue": self.overdue.__repr__()
        }