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

import shutil
import math

# Function Definitions for components
def indexify_weekday(weekday: int) -> int:
    """
    Converts the 0==Monday, 6==Sunday dates
    from *.weekday() to 0==Sunday, 6==Saturday dates
    """

    match weekday:
        case 6:
            return 0
        case _:
            return weekday+1

def fprint(string: str, padding: int = 1, flowtext: bool = True) -> None:
    """
    Print out a string, omitting overflowed text based
    on the terminal width.
    """

    term_width = shutil.get_terminal_size().columns - 2 - padding
    overflow = '…' if flowtext and (len(string) + padding) > term_width else ''
    text_padding: str = " "*padding

    print(f"{text_padding}{string[0:term_width]}{overflow}")

def print_center(string: str, width: int, bias_left: bool = True, return_string: bool = False) -> None | str:
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