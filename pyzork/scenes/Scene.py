import os
import importlib.resources as resources

from . import screen_data

class Scene:
    def __init__(self, name):
        self.name = name

    def set_scene(self):
        screne_text = resources.read_text(screen_data, f'{self.name}.pzk')
        print(screne_text)

    def check_std_opts(self, input_raw):
        cleaned_input = input_raw.strip().lower()

        if cleaned_input == "":
            print("TODO")
        elif cleaned_input == "x":
            print("exiting")