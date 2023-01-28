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

# Imports
import colorama

# Class Definitions

# Color Classes
class Color:
    """
    Base Class for a color.
    """

    fg: str # Colorama Color
    bg: str # Colorama Color
    name: str = "Color Base Class"

    def colorprint(self, text: str, mode: str = "Fore", return_string: bool = False) -> str | None:
        match mode:
            case "Fore":
                if return_string:
                    return f"{self.fg}{text}{colorama.Fore.RESET}"
                print(f"{self.fg}{text}{colorama.Fore.RESET}")
            case "Back":
                if return_string:
                    return f"{self.bg}{text}{colorama.Back.RESET}"
                print(f"{self.bg}{text}{colorama.Back.RESET}")
            case _:
                try:
                    return self.colorprint(text, mode="Fore", return_string=return_string) # rerun function as fore
                except RecursionError:
                    print("Fatal: recursion error occured!")

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

class Colors:
    black   =   Black
    red     =   Red
    green   =   Green
    yellow  =   Yellow
    blue    =   Blue
    magenta =   Magenta
    cyan    =   Cyan
    white   =   White
    fg_end  =   colorama.Fore.RESET
    bg_end  =   colorama.Back.RESET

class Styles:
    bold    =   colorama.Style.BRIGHT
    dim     =   colorama.Style.DIM
    end     =   colorama.Style.RESET_ALL

# Function Definitions

def get_color_class_from_name(name: str) -> Color: # type: ignore
        """
        Return the Color class, based on its name.
        """

        match name:
            case "black":
                return Black()
            case "red":
                return Red()
            case "green":
                return Green()
            case "yellow":
                return Yellow()
            case "blue":
                return Blue()
            case "magenta":
                return Magenta()
            case "cyan":
                return Cyan()
            case "white":
                return White()
            case _:
                return White()