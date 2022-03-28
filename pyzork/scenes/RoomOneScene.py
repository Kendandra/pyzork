# Display first room
from pyzork.scenes.Scene import Scene

class RoomOneScene(Scene):
    def __init__(self):
        self.name = "room_1"

    def run_scene(self):
        usr_input = input()

        self.check_std_opts(usr_input)
