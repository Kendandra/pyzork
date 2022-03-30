from pyzork import data
from pyzork.director import Director
from pyzork.scene import Scene
from .helpers import clear_screen;
import importlib.resources as resources
import json
import sys

# Entry point.  Responsible for loading all configs and creating the director.
def main():

    clear_screen()

    config_json = resources.read_text(data, 'data.json')

    room_data = load_room_data(config_json)
    command_data = load_command_data(config_json)

    # TODO still need non-display settings with the new Director?
    settings = dict(
        debug=False, # When True, will omit game render and just do debug lines
        display=dict(
            use_unicode=check_system_console_support(),
            max_width=50
        ))

    director = Director(settings, room_data, command_data)

    director.direct()


def load_room_data(json_data):
    return json.loads(json_data)["rooms"]

def load_command_data(json_data):
    return json.loads(json_data)["commands"]

def check_system_console_support():
    # The windows console is garbage, so we can't display "high rez" pictures if we're there
    # Test support for expanded code sets.
    try:
        '┌┬┐╔╦╗╒╤╕╓╥╖│║─═├┼┤╠╬╣╞╪╡╟╫╢└┴┘╚╩╝╘╧╛╙╨╜'.encode(sys.stdout.encoding)
        return True
    except UnicodeEncodeError:
        return False