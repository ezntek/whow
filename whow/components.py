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
from colors import Colors, Styles
import datetime
import calendar
import toml
import os

# other imports
import util
from config import Config
from dataclasses import dataclass

def clear_none(l: list) -> list: # type: ignore
    for count, element in enumerate(l): # type: ignore
        l.pop(count) if element is None else None
    return l # type: ignore

class ScheduleComponent():
    def __init__(self, cfg: Config = Config()) -> None:
        pass

    def __repr__(self) -> str:
        return("pretend this is schedule")

class EventsComponent():
    def __init__(self, cfg: Config = Config()) -> None:
        self.events: list[util.EventEntry] = []
        self.load_events()
    
    def load_events(self) -> None:
        for filename in os.listdir(os.path.join(Config().data_tree_dir, "events")):
            if filename != "index.toml":
                with open(os.path.join(Config().data_tree_dir, "events", filename), "r") as t:
                    self.events.append(util.parse_evententry_from_dict(toml.loads(t.read()), os.path.splitext(filename)[0].replace("_", " ")))

    def datedisplay(self, event: util.EventEntry) -> str:
        return f"{Colors.white()} {event.event_from.__repr__()} {Styles.end}"
        
    def __repr__(self) -> str:
        retval: str = ""
        retval += f"{Styles.bold}Events{Styles.end}"

        categories_string: str = ""

        for event in self.events:
            retval += self.datedisplay(event)
            for category in event.categories:
                categories_string += f"{category.__repr__()} "
            retval += util.fprint(f"{Styles.bold}#{event.index} {self.datedisplay(event)} {categories_string}")

        return retval

class ToDoComponent():
    def __init__(self, cfg: Config) -> None:
        self.todos: list[util.ToDoEntry] = []
        self.important_todos: list[util.ToDoEntry] = []
        self.load_todos()
        self.show_important: bool = False
        self.cfg = cfg

    def load_todos(self) -> None:
        for filename in os.listdir(os.path.join(Config().data_tree_dir, "todos")):
            if filename != "index.toml":
                    todo = util.parse_todoentry_from_dict(toml.load(os.path.join(Config().data_tree_dir, "todos", filename), "r"), os.path.splitext(filename)[0].replace("_", " ")) # type: ignore

                    if util.parse_category_from_name("! important", self.cfg) in todo.categories:
                        self.important_todos.append(todo)
                    else:
                        self.todos.append(todo)

    def __repr__(self) -> str:
        retval: str = ""
        retval += f"{Styles.bold}To-Do's{Styles.end} \n"

        categories_string: str = ""
        
        for todo in self.todos:
            for category in todo.categories:
                categories_string += f"{category.__repr__()} "
            retval += util.fprint(f"{Styles.bold}#{todo.index} {categories_string}{Styles.end} {todo.name}\n")
        return retval

class ImportantComponent():
    def __repr__(self) -> str:
        return ""

class DateDisplay():
    def __init__(self, cfg: Config = Config()) -> None:
        # set up the base variable
        self.date_time_now = datetime.datetime.now()

        # data
        self.date = self.date_time_now.strftime("%A, %B %d %Y")
        self.time = self.date_time_now.strftime("%H:%M:%S")

    def __repr__(self) -> str:
        return f"{Styles.bold}Today is{Styles.end} {Styles.bold}{Colors.blue.bg}{util.emoji('📅')} {self.date}{Styles.end} {Styles.bold}{Colors.magenta.bg}{util.emoji('🕓')} {self.time}{Styles.end}"

@dataclass
class Separator():
    """
    Neat little seperator widget.
    Available Modes: line, equals or tilde
    """

    cfg: Config
    length: int = 27

    def __repr__(self) -> str:
        match self.cfg.default_separator:
            case "line":
                return "-"*self.length
            case "equals":
                return "="*self.length
            case "tilde":
                return "~"*self.length
            case _:
                return ""

@dataclass
class CalDate:
    date: int
    tags: list[util.Category]
    bg: str = ""

    def __repr__(self) -> str:
        return f"{self.bg}{self.date}{Styles.end}"

class Calendar():
    def __init__(self, cfg: Config = Config()) -> None:
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

        # print the days of the week
        for count, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            if count == 6:
                print(f"{Styles.bold}{day}{Styles.end}") # print the \n on the last line
            else:
                print(f"{Styles.bold}{day}{Styles.end} ", end="") # dont print the \n


        # print the dates
        retval = ""
        for y in self.cal:
            for x in y:
                if len(str(x.date)) == 1:
                    if x.date == 0:
                        retval += f"    " # Four Spaces
                    else:
                        retval += f"  {x.__repr__()} " if datetime.datetime.now().date().day != x.date else f"{Colors.white.bg}  {x.__repr__()} {Colors.fg_end}" # 2 then 1 space
                else:
                    retval += f" {x.__repr__()} " if datetime.datetime.now().date().day != x.date else f"{Colors.white.bg} {x.__repr__()}" # 1 on either side
            retval += "\n"
        return retval

# Function definitions
def match_name_with_component(name: str, config: Config = Config()) -> (  DateDisplay          | EventsComponent
                                                             | ImportantComponent   | ToDoComponent
                                                             | ScheduleComponent    | Separator
                                                             | Calendar):
    """
    Return a component class based on its name (str).
    """
    match name.lower():
        case "separator":
            return Separator(config)
        case "calendar":
            return Calendar(config)
        case "datetime":
            return DateDisplay(config)
        case "events":
            return EventsComponent(config)
        case "todos":
            return ToDoComponent(config)
        case "schedule":
            return ScheduleComponent(config)
        case "important":
            return ImportantComponent()
        case _:
            raise NameError(f"Section \"{name}\" not found!")
    
def build_component_list(config: Config = Config()) -> list[DateDisplay | EventsComponent | ImportantComponent | ToDoComponent | ScheduleComponent | Separator | Calendar]:
    """
    Return a list of components based on user's configuration.
    """
    return [match_name_with_component(s, config) for s in Config().sections]