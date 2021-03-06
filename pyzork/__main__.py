import os
from pyzork import data
from pyzork.director import Director
from .helpers import clear_screen;
import importlib.resources as resources
import json
import sys

# Entry point.  Responsible for loading all configs and creating the director.
def main():

    clear_screen()
    try:
        menu_data = load_config_file_to_dict("menus.json", "menus")
        room_data = load_config_file_to_dict("rooms.json", "rooms")
        command_data = load_config_file_to_dict("commands.json", "commands")
        item_data = load_config_file_to_dict("items.json", "items")
        conversation_data = load_config_file_to_dict("conversations.json", "conversations")

        game_data = {
            "menus": menu_data,
            "rooms": room_data,
            "commands": command_data,
            "items": item_data,
            "conversations": conversation_data
        }

        supports_truecolor = check_supports_color()

        settings = {
            "debug": False, # When True, will omit game render and just do debug lines
            "graphics": "high" if supports_truecolor else "low",
            "display": {
                "use_unicode": check_system_console_support(),
                "use_truecolor": supports_truecolor,
                "use_256color": False,
                "use_8color": not supports_truecolor,
                "max_width": 50
            }
        }
    except:
        print("LOAD ERROR")
        return

    director = Director(settings, game_data)

    director.direct()


def load_config_file_to_dict(file_name, json_key):
    try:
        json_data = resources.read_text(data, file_name)
        return json.loads(json_data)[json_key]
    except:
        print(f"Could not load configuration for {json_key}")
        raise Exception("Could not load configuration data.", file_name, json_key)


def check_system_console_support():
    # The windows console is garbage, so we can't display "high rez" pictures if we're there
    # Test support for expanded code sets.
    try:
        '┌┬┐╔╦╗╒╤╕╓╥╖│║─═├┼┤╠╬╣╞╪╡╟╫╢└┴┘╚╩╝╘╧╛╙╨╜'.encode(sys.stdout.encoding)
        return True
    except UnicodeEncodeError:
        return False

def check_supports_color():
    # Returns True if the running system's terminal supports color, and False
    # otherwise.
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty