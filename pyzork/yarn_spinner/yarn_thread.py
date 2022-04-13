

from enum import Enum


class YarnThread:
    """
    YarnThreads are sub-components of YarnNodes containing dialog in an ordered fashion.
    They may contain conditions, or non-dialog meta-instructions
    """
    def __init__(self, raw_text=None) -> None:
        self.raw_parse_text = None


class YarnDialog(YarnThread):
    def __init__(self, speaker, text_with_attributes, tokens, raw_text=None) -> None:
        self.raw_parse_text = raw_text

        self.speaker = speaker
        self.text_with_attributes = text_with_attributes
        self.tokens = tokens

    def __str__(self) -> str:
        return f"{self.speaker}: {'|'.join([token.__str__() for token in self.tokens])}"


class YarnCommand(YarnThread):
    """
    A command in the Yarn Spinner system
    """
    def __init__(self, name, param, raw_text) -> None:
        self.raw_parse_text = raw_text

        self.command_name = name
        self.command_param = param

    def __str__(self) -> str:
        return f"<<{self.command_name} {self.command_param}>>"



class YarnToken:
    """
    A token inside a yarn dialog
    """
    def __init__(self, kind, value) -> None:
        self.kind = kind
        self.parameter = value

    def __str__(self) -> str:
        return f"[{self.kind.name}={self.parameter}]"

class YarnTokenKind(Enum):
    """
    Yarn token enums, contains the full list of markup attributes
    """
    UNKNOWN = 0
    TEXT = 1
    KEYWORD = 2
    STRONG = 3
    MOOD = 4
    WAIT = 5
    SPEED = 6
    COLOR = 7