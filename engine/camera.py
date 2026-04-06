import py5
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self):
        self.rotation = 0

    def set_rotation(self, rotation):
        self.rotation = rotation

    def begin_draw(self):
        py5.push()
        py5.translate(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        py5.rotate(py5.radians(self.rotation))
        py5.translate(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2)

    def end_draw(self):
        py5.pop()
