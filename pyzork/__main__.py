import os
from .data import config
from .data import yarns
from .director import Director
from .yarn_spinner import yarn_parser
from .helpers import clear_screen;
import importlib.resources as resources
import json
import sys

debug = True
yarn_debug = True

# Entry point.  Responsible for loading all configs and creating the director.
def main():

    try:
        supports_truecolor = check_supports_color()

        settings = {
            "debug": debug, # When True, will omit game render and just do debug lines
            "yarn_debug": yarn_debug,
            "graphics": "high" if supports_truecolor else "low",
            "resize_terminal": {
                "should_resize": False, # TODO Currently doesn't work
                "cols": 80,
                "lines": 50
            },
            "display": {
                "scene_component_whitespace_size": 0,
                "use_unicode": check_system_console_support(),
                "use_truecolor": supports_truecolor,
                "use_256color": False,
                "use_8color": not supports_truecolor,
                "command_max_width": 50,
                "room_max_width": 50,
                "chara_max_width": 35
            }
        }

        # Now load all the game data
        menu_data = load_config_file_to_dict("menus.json", "menus")
        room_data = load_config_file_to_dict("rooms.json", "rooms")
        command_data = load_config_file_to_dict("commands.json", "commands")
        item_data = load_config_file_to_dict("items.json", "items")
        conversation_data = load_config_file_to_dict("conversations.json", "conversations")
        yarn_data = load_yarns(conversation_data)

        game_data = {
            "menus": menu_data,
            "rooms": room_data,
            "commands": command_data,
            "items": item_data,
            "conversations": conversation_data,
            "yarns": yarn_data
        }

        # TODO this needs to be updated to work in windows.
        if settings.get("resize_terminal").get("should_resize"):
            os.system(f'mode con: cols={settings["resize_terminal"]["cols"]} lines={settings["resize_terminal"]["lines"]}')

    except Exception as e:
        print(f"LOAD ERROR.")
        raise e

    if not debug:
        clear_screen()

    director = Director(settings, game_data)

    # Start the game loop
    director.direct()


def load_config_file_to_dict(file_name, json_key):
    try:
        json_data = resources.read_text(config, file_name)
        return json.loads(json_data)[json_key]
    except:
        print(f"Could not load configuration for {json_key}")
        raise Exception("Could not load configuration data.", file_name, json_key)


def check_system_console_support():
    # The windows console is garbage, so we can't display "high rez" pictures if we're there
    # Test support for expanded code sets.
    try:
        '┌┬┐╔╦╗╒╤╕╓╥╖│║─═├┼┤╠╬╣╞╪╡╟╫╢└┴┘╚╩╝╘╧╛╙╨╜'.encode(sys.stdout.encoding)
        supports_unicode = True
    except UnicodeEncodeError:
        supports_unicode = False

    if debug:
        print(f"Unicode:{supports_unicode}")

    return supports_unicode

def check_supports_color():
    # Returns True if the running system's terminal supports color, and False
    # otherwise.
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    supports_truecolor = supported_platform and is_a_tty

    if debug:
        print(f"Truecolor:{supports_truecolor}")

    return supports_truecolor

def load_yarns(conversation_data):
    if debug:
        print("Parsing Yarn files.")

    yarn_data = {}

    for conversation in conversation_data:
        try:
            conversation_id = conversation["id"]
            conversation_name = conversation["name"]
            conversation_yarn = conversation["yarn"]
        except:
            raise Exception("Conversation was missing vital information.", conversation)

        try:
            yarn_text = resources.read_text(yarns, conversation_yarn)
            pass
        except:
            raise Exception("Could not find yarn file for conversation.", conversation)

        try:
            parsed_yarn = yarn_parser.parse_yarn(yarn_text, conversation_name, conversation_yarn)
        except:
            raise Exception("Could not parse yarn for conversation.", conversation)

        yarn_data[conversation_id] = parsed_yarn

        if yarn_debug:
            print(parsed_yarn)

    return yarn_data
