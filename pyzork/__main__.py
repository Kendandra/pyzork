from pyzork import data
from pyzork.scene import Scene
from .helpers import clear_screen;
import importlib.resources as resources
import json

def main():

    clear_screen()

    config_json = resources.read_text(data, 'data.json')

    room_data = load_room_data(config_json)
    command_data = load_command_data(config_json)

    #current_scene = swap_scene("menu", "title")
    #current_scene.set_scene()
    #result = current_scene.run_scene()

    command_data = load_command_data(config_json)
    current_scene = swap_scene("game", room_data[0], command_data)
    current_scene.set_scene()
    result = current_scene.run_scene()


def swap_scene(scene_type, scene_data, command_data):
    clear_screen()

    return Scene(scene_data, command_data)

def load_room_data(json_data):
    return json.loads(json_data)["rooms"]

def load_command_data(json_data):
    return json.loads(json_data)["commands"]
