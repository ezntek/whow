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

import colorama
from . import *

BLACK = Black()
RED = Red()
GREEN = Green()
YELLOW = Yellow()
BLUE = Blue()
MAGENTA = Magenta()
CYAN = Cyan()
WHITE = White()
FG_END = colorama.Fore.RESET
BG_END = colorama.Back.RESET

def from_name(name: str) -> Color:
    """
    Return the Color class, based on its name.
    """

    match name.lower():
        case "black":
            return BLACK
        case "red":
            return RED
        case "green":
            return GREEN
        case "yellow":
            return YELLOW
        case "blue":
            return BLUE
        case "magenta":
            return MAGENTA
        case "cyan":
            return CYAN
        case "white":
            return WHITE
        case _:
            return WHITE