

class YarnThread:
    """
    YarnThreads are sub-components of YarnNodes containing dialog in an ordered fashion.
    They may contain conditions, or non-dialog meta-instructions
    """
    def __init__(self) -> None:
        self.raw_parse_text = None

        self.speaker = None
        self.text_with_attributes = None
        self.text = None
        self.tokens = []




class YarnCommand:
    """
    A command in the Yarn Spinner system
    """
    def __init__(self) -> None:
        self.raw_parse_text = None

        self.command_name
        self.command_param


