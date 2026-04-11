import py5
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

ROTATION_DURATION = 0.25

class Camera:
    def __init__(self):
        self.rotation = 0
        self._display_angle = 0.0
        self._from_angle = 0.0
        self._elapsed = 0.0
        self._animating = False

    def reset(self):
        """Snap immediately to angle 0 with no animation."""
        self.rotation = 0
        self._display_angle = 0.0
        self._from_angle = 0.0
        self._target_angle = 0.0
        self._elapsed = 0.0
        self._animating = False

    def start_rotation(self, new_rotation):
        """Begin animating toward new_rotation (a multiple of 90).

        Delta is measured from _display_angle (where the camera actually is
        right now) so rapid/interrupted spins always land on the correct
        final angle even if the previous animation was mid-way through.
        """
        self._from_angle = self._display_angle
        delta = (float(new_rotation) - self._display_angle) % 360.0
        if delta > 180.0:
            delta -= 360.0
        self._target_angle = self._display_angle + delta
        self.rotation = new_rotation
        self._elapsed = 0.0
        self._animating = True

    def update(self, dt):
        """Advance the animation; returns True when the spin is complete."""
        if not self._animating:
            return True
        self._elapsed += dt
        t = min(self._elapsed / ROTATION_DURATION, 1.0)
        t = t * t * (3 - 2 * t)
        self._display_angle = self._from_angle + (self._target_angle - self._from_angle) * t
        if self._elapsed >= ROTATION_DURATION:
            self._display_angle = self._target_angle
            self._animating = False
            return True
        return False

    def is_animating(self):
        return self._animating

    def begin_draw(self):
        py5.push()
        py5.translate(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        py5.rotate(py5.radians(self._display_angle))
        py5.translate(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2)

    def end_draw(self):
        py5.pop()