from .helpers import clear_screen;
from .scenes.TitleScene import TitleScene
from .scenes.RoomOneScene import RoomOneScene


def main():

    current_scene = swap_scene("title")
    current_scene.set_scene()
    result = current_scene.run_scene()

    # implement quit from title screen at some point :/

    current_scene = swap_scene("room_1")
    current_scene.set_scene()
    result = current_scene.run_scene()


def swap_scene(scene_name):
    clear_screen()

    if scene_name == "title":
        return TitleScene()
    elif scene_name == "room_1":
        return RoomOneScene()
