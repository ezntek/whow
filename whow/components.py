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

# core imports
import colorama
import datetime
import calendar

# other imports
import util
from dataclasses import dataclass

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
class Separator():
    """
    Neat little seperator widget.
    Avaiable Modes: line, equals or tilde
    """

    mode: str = "line" # line, equals or tilde
    length: int = 27

    def __repr__(self) -> str:
        match self.mode:
            case "line":
                return "-"*self.length
            case "equals":
                return "="*self.length
            case "tilde":
                return "~"*self.length
            case _:
                return ""

@dataclass
class Tag:
    name: str | None
    importance: str | None
    color: str | None # colorama color

@dataclass
class CalDate:
    date: int
    tags: list[Tag]
    bg: str = colorama.Back.RESET # colorama bg

    def __repr__(self) -> str:
        return f"{self.bg}{self.date}{END}"

class Calendar():
    def __init__(self) -> None:
        datetime_now = datetime.datetime.now().date()
        monthrange = calendar.monthrange(int(datetime_now.strftime("%Y")), int(datetime_now.strftime("%m")))
        
        self.cal = [[CalDate(0, []) for _ in range(7)] for _ in range(5)]
        
        row_counter = 0
        for day in range(monthrange[1]): # loop over the no. of days in the month
            # increment row counter if last index is filled
            if self.cal[row_counter][6].date != 0:
                row_counter += 1

            # get weekday
            wd = datetime.datetime.strptime(f"{str(day+1)} {datetime_now.month} {datetime_now.year}", "%d %m %Y").weekday()
            
            # set the day
            self.cal[row_counter][util.indexify_weekday(wd)] = CalDate(day+1, [])
    
    def __repr__(self) -> str:
        """
        Some pretty-printing for self.cal.
        """

        # print the month name
        now = datetime.datetime.now().date()
        month_year = now.strftime("%B %Y")
        util.print_center(month_year, 27, bias_left = True)

        # print the dates
        for count, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            if count == 6:
                print(f"{BOLD}{day}{END}") # print the \n on the last line
            else:
                print(f"{BOLD}{day}{END} ", end="") # dont print the \n


        # print the dates
        retval = ""
        for y in self.cal:
            for x in y:
                if len(str(x.date)) == 1:
                    if x.date == 0:
                        retval += f"    " # Four Spaces
                    else:
                        retval += f"  {x.__repr__()} " # 2 then 1 space
                else:
                    retval += f" {x.__repr__()} "# 1 on either side
            retval += "\n"
        return retval