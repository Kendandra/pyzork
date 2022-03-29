import os
import importlib.resources as resources
from .deps.climage import convert



class Scene:
    def __init__(self, data, command_list_data):
        self.name = data["name"]
        self.id = data["id"]
        self.description = data["description"]
        self.image = data["image"]
        self.commands = data["commands"]
        self.command_list_data = command_list_data

    def set_scene(self):
        screen_description = self.description
        screen_visual = self.get_screen_display()
        command_list = [self.get_command_description(command["type"]) for command in self.commands]

        print(f"{screen_description}\n\n{screen_visual}\n{command_list}")

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
        return convert(f'pyzork/data/maps/{image}.png', is_unicode=True, palette="default", width=50)

    def get_command_description(self, command_type):
        command = [command for command in self.command_list_data if command["type"] == command_type]
        return command[0]["description"]

