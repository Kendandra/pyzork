

class Spinner:
    """
    A converstation engine that is generated from the Yarn Spinner format.  Kinda.
    """
    def __init__(self) -> None:

        # I'm making up how to parse this as I go, really.  But the Yarn Spinner format is
        # a pretty great format, that looks pretty easy to parse so....  Why not.

        self.nodes = {}     # Dict of YarnNodes indexed by node name
        pass