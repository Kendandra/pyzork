import os
import importlib.resources as resources
from .deps.climage import convert



class Scene:
    def __init__(self, data):
        self.name = data["name"]
        self.id = data["id"]
        self.description = data["description"]
        self.image = data["image"]

    def set_scene(self):
        screne_text = self.get_screen_display()
        print(screne_text)

    def run_scene(self):
        self.check_std_opts(input())

    def check_std_opts(self, input_raw):
        cleaned_input = input_raw.strip().lower()
        print("yup, got it: " + cleaned_input)

    def get_screen_display(self):
        # if display type == text
        # return resources.read_text(screen_data, f'{self.name}.pzk')
        # if display type == img
        image = self.image

        return convert(f'pyzork/data/maps/{image}.png', is_unicode=True, palette="default")
