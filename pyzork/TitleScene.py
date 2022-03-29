# Display a title screen.  Anykey should advance.
from pyzork.scene import Scene

class TitleScene(Scene):
    def __init__(self):
        self.name = "title"

    def run_scene(self):
        usr_input = input()

        self.check_std_opts(usr_input)
