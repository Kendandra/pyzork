from pyzork.scene import Scene


class RoomScene(Scene):

    def __init__(self, settings, scene_data, command_data):
        if scene_data["type"] != "room":
            raise Exception("Scene called on unsupported data type", scene_data["type"])

        super().__init__(settings, scene_data, command_data)
