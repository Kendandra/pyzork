import os
import importlib.resources as resources
import climage
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
            self.what = scene_data["what"]
            self.name = scene_data["name"]
            self.id = scene_data["id"]
            self.scene_commands = scene_data["commands"]
        except:
            raise Exception("Scene configuration was missing required data.  Check data.json.")

        self.description = scene_data.get("description")
        self.image_render = scene_data.get("image_render")
        self.text_render = scene_data.get("text_render")

        self.display = settings["display"]
        self.graphics = settings["graphics"]
        self.command_prototypes_data = command_data

        # A command list calculated every set_scene, taking into account game/player state.
        self.active_command_tuples = None


    def set_scene(self, prompt="What will you do?", debug_no_display=False):
        screen_description = self.description
        screen_visual = self.get_screen_display()

        # Get commands currently valid for scene (always) and current game/player state (changes)
        self.active_command_tuples = self.get_active_command_tuples()

        command_list = self.get_command_prompt(self.active_command_tuples, prompt)

        # Render the scene
        if debug_no_display:
            print(f"Expected to render {self.what}:{self.id} {self.name}")
        else:
            clear_screen()
            print(f"{screen_description}\n\n{screen_visual}\n{command_list}")

    def run_scene(self):
        if not self.active_command_tuples:
            raise Exception("No valid active commands found for scene.  Scene not set or misconfigured.", self.commands)

        player_command_tuple = None
        while not player_command_tuple:
            command_check_tuple = self.check_player_command_tuple(input())

            if not command_check_tuple:
                clear_screen()
                # Inform the player that we didn't understand.
                self.set_scene(prompt="Try as you might, you cannot.")
            else:
                player_command_tuple = command_check_tuple

        return player_command_tuple

    def check_player_command_tuple(self, input_raw):
        # Remove whitespace and make lowercase, all our verbs are hopefully listed in the config as lowercase
        cleaned_input = input_raw.strip().lower()

        # Search active command prototypes for their list of verbs (alises) find some that match
        possible_command_tuple_matches = [
            command_tuple
            for command_tuple
            in self.active_command_tuples
            if cleaned_input in command_tuple[0]["verbs"]
        ]

        if len(possible_command_tuple_matches) == 0:
            return None
        else:
            # Out of any that matched, find what in the scene the player was probably trying to say
            # Take the first match we find.  TODO: maybe later we'll add a specificity number and order by that?
            return possible_command_tuple_matches[0]


    # TODO When ghost-sense is added, should this move out of the scene display?
    def get_command_prompt(self, command_tuples, prompt):
        spacer = "■"
        ruler = spacer*(self.display["max_width"])
        centered_prompt = prompt.center(self.display["max_width"], " ")
        command_descriptions = '\n'.join([prototype_command["description"] for (prototype_command, _) in command_tuples])

        return f"{ruler}\n{centered_prompt}\n{ruler}\n{command_descriptions}\n{ruler}"


    def get_screen_display(self):
        if self.image_render:
            return climage.convert(f'pyzork/data/maps/{self.image_render}.png',
                is_unicode=self.display["use_unicode"],
                is_truecolor=self.display["use_truecolor"],
                is_256color=self.display["use_256color"],
                palette="default",
                width=self.display["max_width"]
                )
        if self.text_render:
            return resources.read_text(data_files, self.text_render)
        else:
            return ""

    def get_command_prototype(self, command_what):
        command = [command for command in self.command_prototypes_data if command["what"] == command_what][0]

        if len(command) == 0:
            raise Exception("Invalid command configuration for scene.  No valid commands found for command type.", command_what)

        return command[0]

    def get_active_command_tuples(self):

        # Make these lists a bit easier to work with.
        command_prototypes_dict = {command["what"]:command for command in self.command_prototypes_data}
        scene_commands_dict = {command["what"]:command for command in self.scene_commands}

        valid_commands = []

        # Add THIS scene specific commands
        valid_commands = valid_commands + [(command_prototypes_dict[scene_command_what], scene_commands_dict[scene_command_what])
            for scene_command_what
            in scene_commands_dict
            if self.is_command_active(command_prototypes_dict[scene_command_what], scene_commands_dict[scene_command_what])]


        # Now add any commands for scene kind, if we didn't have a scene specific version.
        # TODO Need to figure out this second part better. Code is valid, but probably shouldn't use "on", more like "always_on"?
        """
        valid_commands = valid_commands + [(command_prototypes_dict[command_prototype_what], command_prototypes_dict[command_prototype_what])
            for command_prototype_what
            in command_prototypes_dict
            if self.what in command_prototypes_dict[command_prototype_what]["on"]                                                               # Valid for this scene type
                and self.is_command_active(command_prototypes_dict[command_prototype_what], command_prototypes_dict[command_prototype_what])    # Meets activation requirements
                and command_prototype_what not in [command[0]["what"] for command in valid_commands]                                            # Not already in the command list
        ]
        """

        # Then sort by the "order" field on the prototype
        valid_commands.sort(key=lambda tuple: tuple[0]["order"])

        return valid_commands

    def is_command_active(self, prototype_command, scene_command):

        if not "when" in scene_command and not "when" in prototype_command:
            return True

        # scene activation conditions always first, then global activation conditions
        when_conditions = scene_command["when"] if "when" in scene_command else None
        if when_conditions:
            return self.eval_command_condition(when_conditions)

        when_conditions = prototype_command["when"] if "when" in prototype_command else None

        if when_conditions and self.eval_command_condition(when_conditions):
            return True

        return False

    def eval_command_condition(self, when_conditions):
        # For now assume the conditions are "when any".  Later added fields for "when_all" or "when_any" specifically?
        for when in when_conditions:
            if when["condition"] == "graphics":
                if self.graphics == when["is"]:
                    return True
            else:
                raise Exception("Unknown command-when condition.", when_conditions)

        return False



