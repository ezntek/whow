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

from ..colors import colors, styles

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

class ToDoIndexError(Exception):
    """
    Creates a to-do index error.
    """

    def __init__(self) -> None:
        error("To-Do index error - No To-Do with the index was found.")
    
class NameOrIndexUnwrappingError(Exception):
    """
    Creates a name or index unwrapping error.
    """

def logs(text: str) -> str:
    return f"{styles.BOLD}{colors.YELLOW.sprint('[>>]')}{styles.END} {text}"

def errors(text: str) -> str:
    return f"{styles.BOLD}{colors.RED.sprint('[!!]')}{styles.END} {text}"

def warns(text: str) -> str:
    return f"{styles.BOLD}{colors.MAGENTA.sprint('[!!]')}{styles.END} {text}"

def log(text: str) -> None:
    print(logs(text))

def error(text: str) -> None:
    print(errors(text))

def warn(text: str) -> None:
    print(warns(text))

