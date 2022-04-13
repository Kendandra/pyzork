from .scene import Scene


class RoomScene(Scene):

    def __init__(self, settings, scene_data, command_data):
        if scene_data["what"] != "room":
            raise Exception("Scene called on unsupported data type", scene_data["what"])

        super().__init__(settings, scene_data, command_data)
