# Display a title screen.  Anykey should advance.
from pyzork.scenes.Scene import Scene

class TitleScene(Scene):
    def __init__(self):
        self.name = "title"

    def run_scene(self):
        usr_input = input()

        self.check_std_opts(usr_input)
