from rooms.room import Room
from core.utils import Rect


class DefaultDeadEnd(Room):
    ROOM_TYPE = "dead_end"

    def setup(self):
        self.platforms += [
            Rect(180, 250, 180, 20),
            Rect(360, 370, 180, 20),
            Rect(180, 490, 180, 20),
        ]


VARIANTS = [DefaultDeadEnd]
