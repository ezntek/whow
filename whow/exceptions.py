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

from colors import Styles, Colors

# function definitions

def log(text: str, return_string: bool = False) -> None | str:
    return f"{Styles.bold}{Colors.yellow().colorprint('[>>]', return_string=True)}{Styles.end} {text}" if return_string else print(f"{Styles.bold}{Colors.yellow().colorprint('[>>]', return_string=True)}{Styles.end} {text}")

def error(text: str, return_string: bool = False) -> None | str:
    return f"{Styles.bold}{Colors.red().colorprint('[!!]', return_string=True)}{Styles.end} {text}" if return_string else print(f"{Styles.bold}{Colors.red().colorprint('[!!]', return_string=True)}{Styles.end} {text}")

def warn(text: str, return_string: bool = False) -> None | str:
    return f"{Styles.bold}{Colors.magenta().colorprint('[!!]', return_string=True)}{Styles.end} {text}" if return_string else print(f"{Styles.bold}{Colors.magenta().colorprint('[!!]', return_string=True)}{Styles.end} {text}")

# class definitions

class InvalidMonthNameError(Exception):
    """
    Complains about an invalid month name.
    """
    
    def __init__(self) -> None:
        "Constructs the invalid month name complaint."

        error("Invalid Month Name - It has to be any one of Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, or Dec.")
        exit(1)

class DateFormattingError(Exception):
    """
    Complains about a date formatting error.
    """
   
    def __init__(self) -> None:
        "Constructs the date formatting complaint."

        error("Invalid Date Formatting - the date must be formatted in either the mm/dd/YYYY, YYYY/mm/dd, or Month day, Year format.")
        exit(1)

class FatalError(Exception):
    """
    Creates a fatal error.
    """

    def __init__(self, text: str) -> None:
        error(text)
        exit(1)