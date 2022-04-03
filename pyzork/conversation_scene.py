from importlib import resources
from .scene import Scene
from .data import templates as templates
import climage


class ConversationScene(Scene):

    def __init__(self, settings, scene_data, command_data):
        if scene_data["what"] != "conversation":
            raise Exception("Scene called on unsupported data type", scene_data["what"])

        super().__init__(settings, scene_data, command_data)

        self.image_render = "crow1"


    def get_screen_display(self):
        if self.image_render:
            return climage.convert(f'pyzork/data/chara/{self.image_render}.png',
                is_unicode=self.display["use_unicode"],
                is_truecolor=self.display["use_truecolor"],
                is_256color=self.display["use_256color"],
                is_8color=self.display["use_8color"],
                palette="default",
                width=self.display["chara_max_width"]
                )
        if self.text_render:
            return resources.read_text(templates, self.text_render)
        else:
            return ""
