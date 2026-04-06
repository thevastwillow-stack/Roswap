from rooms.room import Room
from core.utils import Rect


class DefaultPlus(Room):
    ROOM_TYPE = "plus"

    def setup(self):
        self.platforms += [
            Rect(270, 270, 180, 20),
            Rect(270, 450, 180, 20),
        ]


VARIANTS = [DefaultPlus]
