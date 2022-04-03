
from .actor import Actor


class PlayerActor(Actor):

    def __init__(self):
        self.inventory = None
        self.room_location = None
        super().__init__()
        pass