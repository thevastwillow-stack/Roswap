from rooms.room import Room
from core.utils import Rect


class DefaultTJunction(Room):
    ROOM_TYPE = "t_junction"

    def setup(self):
        self.platforms += [
            Rect(240, 300, 240, 20),
            Rect(120, 460, 180, 20),
            Rect(420, 460, 180, 20),
        ]


VARIANTS = [DefaultTJunction]
