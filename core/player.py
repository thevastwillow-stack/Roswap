import py5
import random
import colorsys
from core.utils import Rect
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WALL, GAP, GAP_START, GAP_END, COLORS

_EXIT_DEPTH = 16
_LIGHT_MARGIN = WALL + 80
_LIGHT_RINGS = 6
_LIGHT_MAX_RADIUS = 180


class Room:
    def __init__(self, openings):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.openings = openings
        self.platforms = []
        self.exit_zones = {}
        self.exit_zones["north"] = None
        self.exit_zones["south"] = None
        self.exit_zones["east"] = None
        self.exit_zones["west"] = None

        m = _LIGHT_MARGIN
        self.light_x = random.randint(m, SCREEN_WIDTH - m)
        self.light_y = random.randint(m, SCREEN_HEIGHT - m)
        h = random.random()
        r, g, b = colorsys.hsv_to_rgb(h, 0.85, 1.0)
        self.light_color = (int(r * 255), int(g * 255), int(b * 255))

        self._build_walls()
        self.setup()
        self._build_exit_zones()

    def _wall(self, *args):
        self.platforms.append(Rect(*args))

    def _build_walls(self):
        D = self.width
        W = WALL
        S = GAP_START
        E = GAP_END

        if self.openings.get("north"):
            self._wall(0, 0, S, W)
            self._wall(E, 0, D - E, W)
        else:
            self._wall(0, 0, D, W)

        if self.openings.get("south"):
            self._wall(0, D - W, S, W)
            self._wall(E, D - W, D - E, W)
        else:
            self._wall(0, D - W, D, W)

        if self.openings.get("west"):
            self._wall(0, 0, W, S)
            self._wall(0, E, W, D - E)
        else:
            self._wall(0, 0, W, D)

        if self.openings.get("east"):
            self._wall(D - W, 0, W, S)
            self._wall(D - W, E, W, D - E)
        else:
            self._wall(D - W, 0, W, D)

    def _build_exit_zones(self):
        D = self.width
        t = _EXIT_DEPTH
        if self.openings.get("north"):
            self.exit_zones["north"] = Rect(GAP_START, 0, GAP, t)
        if self.openings.get("south"):
            self.exit_zones["south"] = Rect(GAP_START, D - t, GAP, t)
        if self.openings.get("west"):
            self.exit_zones["west"] = Rect(0, GAP_START, t, GAP)
        if self.openings.get("east"):
            self.exit_zones["east"] = Rect(D - t, GAP_START, t, GAP)

    def setup(self):
        """Add interior platforms via self.platforms.append(Rect(...))."""

    def spawn_point(self, entry_direction):
        cx = self.width // 2 - 15
        cy = self.height // 2 - 22
        inset = WALL + 80

        if entry_direction == "north":
            return (cx, inset)
        elif entry_direction == "south":
            return (cx, self.height - inset - 45)
        elif entry_direction == "east":
            return (self.width - inset - 30, cy)
        elif entry_direction == "west":
            return (inset, cy)
        else:
            return (cx, cy)

    def get_platforms(self):
        return self.platforms

    def check_exit(self, player_rect):
        for direction, zone in self.exit_zones.items():
            if zone and player_rect.colliderect(zone):
                return direction
        return None

    def draw(self):
        py5.no_stroke()
        py5.background(*COLORS["background"])
        self._draw_light()
        py5.fill(*COLORS["platform"])
        for p in self.platforms:
            py5.rect(p.x, p.y, p.w, p.h)
        py5.fill(*COLORS["exit_zone"], 80)
        for zone in self.exit_zones.values():
            if zone:
                py5.rect(zone.x, zone.y, zone.w, zone.h)

    def _draw_light(self):
        lx, ly = self.light_x, self.light_y
        lr, lg, lb = self.light_color

        py5.no_stroke()
        for i in range(_LIGHT_RINGS, -1, -1):
            t = i / _LIGHT_RINGS
            radius = _LIGHT_MAX_RADIUS * t
            alpha = int((1.0 - t) ** 2.5 * 100)
            py5.fill(lr, lg, lb, alpha)
            py5.ellipse(lx, ly, radius * 2, radius * 2)

        py5.fill(lr, lg, lb, 230)
        py5.ellipse(lx, ly, 12, 12)