from rooms.room import Room
from core.utils import Rect


class DefaultCorridor(Room):
    ROOM_TYPE = "corridor"

    def setup(self):
        self.platforms += [
            Rect(150, 300, 180, 20),
            Rect(390, 420, 180, 20),
        ]


VARIANTS = [DefaultCorridor]
