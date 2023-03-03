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

# imports
import colorama
import typing

class Color:
    """
    Base Class for a color.
    """
    
    fg: str
    bg: str
    name: str = "Color Base Class"

    def sprint(self, text: str, mode: typing.Literal["fore"] | typing.Literal["back"] = "fore") -> str:
        match mode:
            case "fore":
                return f"{self.fg}{text}{colorama.Fore.RESET}"
            case "back":
                return f"{self.bg}{text}{colorama.Back.RESET}"
    
    def print(self, text: str, mode: typing.Literal["fore"]| typing.Literal["back"] = "fore") -> None:
        print(self.sprint(text, mode))

class Black(Color):
    name = "Black"

    fg = colorama.Fore.BLACK
    bg = colorama.Back.BLACK

class Red(Color):
    name = "Red"

    fg = colorama.Fore.RED
    bg = colorama.Back.RED

class Green(Color):
    name = "Green"

    fg = colorama.Fore.GREEN
    bg = colorama.Back.GREEN

class Yellow(Color):
    name = "Yellow"

    fg = colorama.Fore.YELLOW
    bg = colorama.Back.YELLOW

class Blue(Color):
    name = "Blue"

    fg = colorama.Fore.BLUE
    bg = colorama.Back.BLUE

class Magenta(Color):
    name = "Magenta"

    fg = colorama.Fore.MAGENTA
    bg = colorama.Back.MAGENTA

class Cyan(Color):
    name = "Cyan"

    fg = colorama.Fore.CYAN
    bg = colorama.Back.CYAN

class White(Color):
    name = "White"

    fg = colorama.Fore.WHITE
    bg = colorama.Back.WHITE

