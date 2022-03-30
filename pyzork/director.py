from pyzork.menu_scene import MenuScene
from pyzork.room_scene import RoomScene
from pyzork.scene import Scene

# Responsible for loading scenes, processing commands,
# Owns all actors.
class Director:
    def __init__(self, settings, menu_data, room_data, command_data):
        self.settings = settings
        self.menu_data = menu_data
        self.room_data = room_data
        self.command_data = command_data

        self.current_scene = None
        self.actor_player = None # TODO Make a player to track inventory state

        # Start the game on the title-menu
        self.next_scene_request = ("menu", menu_data[0]["id"])


    def direct(self):
        while True:
            next_scene = self.get_next_scene()

            if (not not next_scene
                or next_scene.id != self.current_scene.id
                or next_scene.type != self.current_scene.type):
                self.current_scene = next_scene
                self.current_scene.set_scene(debug_no_display=self.settings["debug"])

                if self.settings["debug"]:
                    print(f"Next scene found: {self.current_scene.name}")

            player_command = self.current_scene.run_scene()

            if self.settings["debug"]:
                print(f"Got command {player_command}")

            should_exit = self.execute_player_command(player_command)

            if should_exit:
                break

        # TODO replace with a "goodbye" scene?
        return "Thanks for playing!"

    def execute_player_command(self, player_command):
        # First find the command prototype for this player_command
        command_prototype = next(iter([command for command in self.command_data if player_command["type"] == command["type"]]), None)

        if not command_prototype:
            raise Exception("Could not find command prototype for player_command", player_command)

        command_kind = command_prototype["kind"]

        if command_kind == "move-to-target":
            # get the target to set the scene
            room_target = player_command["target"]
            self.next_scene_request = ("room", room_target)
        elif command_kind == "menu-game-exit":
            # Special command that exits the while loop.
            return True
        elif command_kind == "menu-game-start":
            # Special command that always goes to room-1
            self.next_scene_request = ("room", 1)
        else:
            raise Exception("Unknown command kind", command_kind)

        return False


    def get_next_scene(self):
        if not self.next_scene_request:
            return self.current_scene

        (next_scene_type, next_scene_id) = self.next_scene_request

        if not next_scene_type or not next_scene_id:
            return self.current_scene

        if next_scene_type == "room":
            next_scene_data = next(iter([room for room in self.room_data if room["id"] == next_scene_id]), None)

            if not next_scene_data:
                raise Exception("No scene data found for id", next_scene_id)

            scene = RoomScene(
                settings=self.settings,
                scene_data=next_scene_data,
                command_data=self.command_data)

        elif next_scene_type == "menu":
            next_scene_data = next(iter([menu for menu in self.menu_data if menu["id"] == next_scene_id]), None)

            if not next_scene_data:
                raise Exception("No scene data found for id", next_scene_id)

            scene = MenuScene(
                settings=self.settings,
                scene_data=next_scene_data,
                command_data=self.command_data)

        else:
            raise Exception("Unknown scene type", next_scene_type)

        # Clear out pending scene requests
        self.next_scene_id = ()

        return scene
