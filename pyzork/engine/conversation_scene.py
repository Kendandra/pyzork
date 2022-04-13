"""_summary_

Raises:
    Exception: _description_

Returns:
    _type_: _description_
"""
from importlib import resources
import typing
import climage
from .errors import InvalidSceneDataError
from .scene import Scene
from ..data import templates

class ConversationScene(Scene):
    """_summary_

    Args:
        Scene (_type_): _description_
    """

    def __init__(self,
                settings: typing.Dict[str, object],
                scene_data: typing.Dict[str, object],
                command_data: typing.Dict[str, object]) -> None:
        """ Inits a ConversationScene.

        Args:
            settings (typing.Dict[str, object]): Global game settings dictionary
            scene_data (typing.Dict[str, object]): Data specific to rendering this scene object.
                                                   Must be a "what" of "conversation".
            command_data (typing.Dict[str, object]): Command prototype data.

        Raises:
            Exception: _description_
        """
        if scene_data["what"] != "conversation":
            raise InvalidSceneDataError("Scene called on unsupported data type",
                                            scene_data["what"])

        super().__init__(settings, scene_data, command_data)

        self.image_render = "crow1"


    def get_screen_display(self) -> str:
        """ Generates a screen display for a conversation.  This includes pictures or UI.

        Returns:
            str: render string, intended to be printed to the console
        """
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
