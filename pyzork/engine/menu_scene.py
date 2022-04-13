from pyzork.engine.errors import InvalidSceneDataError
from pyzork.engine.scene import Scene


class MenuScene(Scene):

    def __init__(self, settings, scene_data, command_data):
        if scene_data["what"] != "menu":
            raise InvalidSceneDataError("Scene called on unsupported data type", scene_data["what"])

        super().__init__(settings, scene_data, command_data)

