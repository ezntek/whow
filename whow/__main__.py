#    Whow 
#    A rewrite of DaringCuteSeal/whow in Python that aims to polish the overall UX.

#    Copyright (C) 2023 ezntek (ezntek@xflymusic.com) and <placeholder>

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
import os
import sys

# Constant Definitions
__version__ = "0.1.0"
BOLD = '\033[1m'
END = '\033[0m'
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

# Function Definitions
def log(text: str) -> None:
    print(f"{colorama.Fore.YELLOW}{BOLD}LOG: {END}{text}")

def error(text: str) -> None:
    print(f"{colorama.Back.RED}{BOLD}{colorama.Fore.WHITE}ERROR:{END} {text}")

def warn(text: str) -> None:
    print(f"{colorama.Fore.RED}{BOLD}WARNING:{END} {text}")

def print_help() -> None:
    # open the help file in the resources folder
    
    with open(os.path.join(CURRENT_PATH, "./res/help.txt")) as helptxt:
        print(helptxt.read())

def show() -> None:
    pass

# Main Function
def main() -> None:
    try:
        match sys.argv[1:]: # string slicing magic
            case ["-h"]:
                print_help()
            case ["-V"]:
                print(__version__)
            case ["-c"]:
                pass # placeholder
            case _: # default option (no arguments)
                show()

    except KeyboardInterrupt:
        log("Interrupt signal received, quitting..")
        sys.exit()
    
# Driver Code
if __name__ == "__main__":
    main()