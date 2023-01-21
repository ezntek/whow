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

# Core Imports
import util
import os
import sys

# Other imports
import components as cmp

# Constant Definitions
__version__ = "0.1.0"
BOLD = '\033[1m'
END = '\033[0m'
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

# Function Definitions
def print_help() -> None:
    # open the help file in the resources folder
    
    with open(os.path.join(CURRENT_PATH, "./res/help.txt")) as helptxt:
        print(helptxt.read())

def parse_args() -> None:
    # do some sys.argv parsing here
    
    match sys.argv[1:]: # string slicing magic
            case ["-h"]:
                print_help()
            case ["-V"]:
                print(__version__)
            case ["-c"]:
                pass # placeholder
            case _: # default option (no arguments)
                show()

def show() -> None:
    print(cmp.Separator(length=55))
    print(cmp.DateDisplay())
    print(cmp.Separator(length=55))
    print(cmp.Calendar())
    print(cmp.Separator(mode="equals", length=55))
    
# Main Function
def main() -> None:
    try:
        parse_args()        
    except KeyboardInterrupt:
        util.log("Interrupt signal received, quitting..")
        sys.exit()
    
# Driver Code
if __name__ == "__main__":
    main()
