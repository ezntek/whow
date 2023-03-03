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

import math
import shutil
import datetime

from ..exceptions import *
from ..config import *

def clean_empty_strings_in_list(l: list[str]) -> list[str]:
    for count, element in enumerate(l):
        l.pop(count) if element == "" else None
    return l

def indexify_weekday(weekday: int) -> int:
    """
    Converts the 0==Monday, 6==Sunday dates
    from *.weekday() to 0==Sunday, 6==Saturday dates
    """

    return 0 if weekday == 6 else weekday+1

def emoji(emoji: str, cfg: Config = Config()) -> str | None:
    """
    Print out an emoji if `enable_emojis` is set to true on the configuration.
    """
    if cfg.enable_emojis:
        return emoji

def sfprint(string: str, padding: int = 0, flowtext: bool = True) -> str:
    """
    Return a string, omitting overflowed text based
    on the terminal width.
    """

    term_width = shutil.get_terminal_size().columns - 2 - padding
    overflow = '…' if flowtext and (len(string) + padding) > term_width else ''
    text_padding: str = " "*padding

    return(f"{text_padding}{string[0:term_width]}{overflow}")

def print_center(string: str, width: int, bias_left: bool = True, return_string: bool = False) -> typing.Union[str, None]:
    """
    Center out a string in a given area (width: int)
    and print that string in the center of that area.
    If the total padding is odd, set the bias variable
    to either "left" or "right" to give one more whitespace
    to that direction.
    """

    padding_width = width - len(string)

    if padding_width % 2 == 1: # check for if padding_width is odd
        # Calculate the padding based on the kwarg
        l_padding_width = math.ceil(padding_width/2) if bias_left else math.floor(padding_width/2)
        r_padding_width = padding_width - l_padding_width

        # print
        if return_string:
            return f"{' '*l_padding_width}{string}{' '*r_padding_width}"
        print(f"{' '*l_padding_width}{string}{' '*r_padding_width}")
    elif padding_width % 2 == 0:
        if return_string:
            return f"{' '*int(padding_width/2)}{string}{' '*int(padding_width/2)}"
        print(f"{' '*int(padding_width/2)}{string}{''*int(padding_width/2)}")

# Datetime Handling
def unify_date_formats(string: str) -> str:
    # The time format stays uniform, whereas
    # there are multiple supported date formats,
    # such as:
    #
    # dd/mm/YYYY
    # YYYY/mm/dd
    # MTH dd YYYY (e.g. Jan 09 2069) or MTH dd, YYYY
    
    CONVERSION_TABLE = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12
    }

    whitespace_split_string = string.split(" ")
    if len(whitespace_split_string) == 3:
        for k, v in CONVERSION_TABLE.items():
            if whitespace_split_string[0].lower() == k:
                return f"{whitespace_split_string[1].replace(',', '')}/{str(v)}/{whitespace_split_string[2]}"
        return ""
    if len(whitespace_split_string) == 2:
        if "," in whitespace_split_string[1]: # "MTH dd,YYYY"
            tmp = whitespace_split_string[1].split(',') # ["dd", 'YYYY"]
            try:
                return f"{tmp[0]}/{CONVERSION_TABLE[whitespace_split_string[0].lower()]}/{tmp[1]}"
            except KeyError:
                raise InvalidMonthNameError()
    del whitespace_split_string

    try:
        split_string = [int(val) for val in string.split("/")]
    except ValueError:
        raise DateFormattingError()
    if split_string[0] > 99:
        return f"{split_string[2]}/{split_string[1]}/{split_string[0]}"
    elif split_string[2] > 99:
        return string

    raise DateFormattingError()

def parse_argv_event_datetime(string: str) -> datetime.datetime:
    # either:
    #   "mm/dd/YYYY 6:09:34 PM" | "mm/dd/YYYY 6:09PM"
    # or:
    #   "mm/dd/YYYY 18:09:34"
    #
    # where seconds can be omitted.
    
    twelve_hour_time: bool = True if "PM" or "AM" in string else False
    afternoon_time: bool = False
    
    s1 = clean_empty_strings_in_list(string.split(" ")) # ["mm/dd/YYYY", "6:09", "PM"] or ["mm/dd/YYYY", "6:09PM"]
    if len(s1) == 3 and s1[-1].lower() == "pm":
        afternoon_time = True
        s1.pop(2) # ["mm/dd/YYYY", "6:09"]
        
    if len(s1) == 2 and s1[-1][-2:].lower() == "pm":
        afternoon_time = True
        s1[-1] = s1[-1][:-2] # ["mm/dd/YYYY", "6:09PM"] -> ["mm/dd/YYYY", "6:09"]
    
    # len(s1) should be 2 by now

    date_part_list = unify_date_formats(s1[0]).split("/")
    time_part_list = s1[1].split(":")

    if twelve_hour_time:
        time_part_list[0] = str(int(time_part_list[0]) + 12) if afternoon_time else time_part_list[0]

    time_part = datetime.time(int(time_part_list[0]), int(time_part_list[1]), int(time_part_list[2])) if len(time_part_list) == 3 else datetime.time(int(time_part_list[0]), int(time_part_list[1]), 0)

    return datetime.datetime(int(date_part_list[2]), int(date_part_list[1]), int(date_part_list[0]), time_part.hour, time_part.minute, time_part.second)

def split_string_date(string_date: str) -> datetime.date:
    """
    Split a string date in the date/month/year format into a datetime.date object.
    """
    string_date_array = string_date.split("/")

    if not string_date:
        return datetime.date(1, 1, 1)

    if (int(string_date_array[0]) > 31) or (int(string_date_array[1]) > 12):
        raise FatalError("The date you supplied was invalid!")
    
    return datetime.date(int(string_date_array[2]), int(string_date_array[1]), int(string_date_array[0]))
