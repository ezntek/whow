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
import colorama
import datetime
import calendar

from dataclasses import dataclass
from typing import Optional

# Idea: Store the date and time in 2 variables and style in the repr
BOLD = '\033[1m'
END = '\033[0m'

class DateDisplay():
    def __init__(self) -> None:
        # set up the base variable
        self.date_time_now = datetime.datetime.now()

        # data
        self.date = self.date_time_now.strftime("%A, %B %d %Y")
        self.time = self.date_time_now.strftime("%H:%M:%S")

    def __repr__(self) -> str:
        return f"{BOLD}Today is{END} {BOLD}{colorama.Back.BLUE}📅 {self.date}{END} {BOLD}{colorama.Back.LIGHTMAGENTA_EX}🕓 {self.time}{END}"

@dataclass
class Seperator():
    mode: str = "line" # line, equals or tilde

    def __repr__(self) -> str:
        match self.mode:
            case "line":
                return "-"*10
            case "equals":
                return "="*10
            case "tilde":
                return "~"*10
            case _:
                return ""

@dataclass
class Tag:
    name: Optional[str]
    importance: Optional[str]
    color: Optional[str] # colorama color

@dataclass
class CalDate:
    date: int
    tags: list[Tag]
    bg: str # colorama bg

    def __repr__(self) -> str:
        return f"{self.bg}{self.date}{END}"

class Calendar():
    def __init__(self) -> None:
        self.days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        datetime_now = datetime.datetime.now().date()
        monthrange = calendar.monthrange(int(datetime_now.strftime("%Y")), int(datetime_now.strftime("%m")))
        # monthrange returns a tuple, given 2023, 1 as the input (Jan 2023), we get (day of the week of the 1st of month, number of days in month)
        self.cal = []
        for day in range(monthrange[1]): # loop over the no. of days in the month:
            pass