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
import os
import sys
import datetime

# Other imports
import util
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
    print(sys.argv[1:])
    match sys.argv[1]: # slicing magic
        case "-h":
            print_help()
        case "-V":
            print(__version__)
        case "-c":
            pass # placeholder
        case "todo":
            match sys.argv[2]:
                case "add":
                    # guard clauses
                    if len(sys.argv) < 4:
                        util.error("You have to put a name for the new todo entry!")
                        exit()
                    name = sys.argv[3]
                    
                    # set some default values
                    categories: list[str] = []
                    category_classes: list[util.Category] = []
                    due_date = ""

                    if len(sys.argv) >= 5:
                        due_date = sys.argv[4]
                    
                    if len(sys.argv) >= 6:
                        categories = sys.argv[5:]
                        if due_date[0] == "@":
                            categories.append(due_date) 
                            due_date = ""

                    for category_name in categories:
                        if not util.check_category_existence(category_name[1:]):
                            util.warn(f"Category {category_name[1:]} does not exist!")
                            exit()
                        
                        category_classes.append(util.match_name_with_category(category_name[1:]))

                    rv = util.register_todo(util.ToDoEntry(
                        name,
                        None if due_date is None else util.split_string_date(due_date),
                        category_classes,
                        overdue = True if util.split_string_date(due_date) < datetime.datetime.today().date() else False
                    ))

                    util.log(rv) if rv is not None else None
                            
                case "del":
                    if len(sys.argv) <= 4:
                        util.warn("Index of todo is required!")

                    index = int(sys.argv[3])
                    if not util.del_todo(index):
                        util.error(f"Failed to delete to-do by index {index}!")

                case "mark":
                    if len(sys.argv) <= 4:
                        util.warn("Index of todo is required!")
                    
                    index = int(sys.argv[3])
                    util.mark_todo(index)

                case _:
                    print_help()
                
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
