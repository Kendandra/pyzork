import os
import importlib.resources as resources
from climage import convert
from .helpers import clear_screen
from pyzork import data as data_files


# Responsible for managing and running a scene.  Right now only supports rooms.
# Has to know about command data, because it is responsible for rendering the
# command list.  Maybe move that to something else?
# TODO Add more scene types by making subclasses and extracting the RoomScene bits
class Scene:
    def __init__(self, settings, scene_data, command_data):

        if not scene_data:
            raise Exception("Missing scene_data", self)

        if not command_data:
            raise Exception("Missing command_data", self)

        if not settings:
            raise Exception("Missing settings", self)

        try:
            self.type = scene_data["type"]
            self.name = scene_data["name"]
            self.id = scene_data["id"]
            self.commands = scene_data["commands"]
        except:
            raise Exception("Scene configuration was missing required data.  Check data.json.")

        self.description = scene_data.get("description")
        self.image_render = scene_data.get("image_render")
        self.text_render = scene_data.get("text_render")

        self.display = settings["display"]
        self.command_list_data = command_data


    def set_scene(self, prompt="What will you do?", debug_no_display=False):
        screen_description = self.description
        screen_visual = self.get_screen_display()
        command_list = self.get_command_prompt(self.commands, prompt)

        # Render the scene
        if debug_no_display:
            print(f"Detected unicode settings {self.display['use_unicode']}")
            print(f"Detected screen settings {self.display['max_width']}")

            print(f"Expected to render {self.type}:{self.id} {self.name}")
        else:
            clear_screen()
            print(f"{screen_description}\n\n{screen_visual}\n{command_list}")

    def run_scene(self):
        player_command = None
        while not player_command:
            command_check = self.check_player_command(input())

            if not command_check:
                clear_screen()
                # Inform the player that we didn't understand.
                self.set_scene(prompt="Try as you might, you cannot.")
            else:
                player_command = command_check

        return command_check

    def check_player_command(self, input_raw):
        # Remove whitespace and make lowercase, all our verbs are hopefully listed in the config
        # as lowercase
        cleaned_input = input_raw.strip().lower()

        # Search all command prototypes for their list of verbs (alises) find some that match
        possible_prototype_commands = [command for command in self.command_list_data if cleaned_input in command["verbs"]]

        # Out of any that matched, find what in the scene the player was probably trying to say
        # Take the first match we find  TODO: maybe later we'll add a specificity number and order by that?
        scene_command = next(
            iter([command for command in self.commands
                    if command["type"] in [prototype["type"] for prototype in possible_prototype_commands]]
            ), None)

        if not scene_command:
            return None
        else:
            return scene_command


    def get_command_prompt(self, commands, prompt):
        spacer = "■"
        ruler = spacer*(self.display["max_width"])
        centered_prompt = prompt.center(self.display["max_width"], " ")
        command_descriptions = '\n'.join([self.get_command_description(command["type"]) for command in commands])

        return f"{ruler}\n{centered_prompt}\n{ruler}\n{command_descriptions}\n{ruler}"


    def get_screen_display(self):
        if self.image_render:
            return convert(f'pyzork/data/maps/{self.image_render}.png',
                is_unicode=self.display["use_unicode"],
                palette="default",
                width=self.display["max_width"])
        if self.text_render:
            return resources.read_text(data_files, self.text_render)
        else:
            return ""


    def get_command_description(self, command_type):
        command = [command for command in self.command_list_data if command["type"] == command_type]

        if len(command) == 0:
            raise Exception("Invalid command configuration for scene.  No valid commands found for command type.", command_type)

        return command[0]["description"]

