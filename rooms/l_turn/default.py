from rooms.room import Room
from core.utils import Rect


class DefaultLTurn(Room):
    ROOM_TYPE = "l_turn"

    def setup(self):
        self.platforms += [
            Rect(200, 220, 160, 20),
            Rect(360, 360, 160, 20),
            Rect(200, 480, 160, 20),
        ]


VARIANTS = [DefaultLTurn]
