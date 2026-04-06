import random
from core.constants import DIFFICULTY_GRID


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"north": True, "south": True, "east": True, "west": True}
        self.cell_type = "unknown"

_DELTA = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
_OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}


def find_neighbour(anchor, direction, playfield_map):
    dx, dy = _DELTA[direction]
    neighbor = (anchor[0] + dx, anchor[1] + dy)
    if neighbor in playfield_map:
        return neighbor
    return None


class MazeGenerator:

    def __init__(self, difficulty):
        self.size = DIFFICULTY_GRID[difficulty]
        self.grid = None
        self.playfield_map = {}

    def generate(self):
        size = self.size

        self.grid = []
        for gy in range(size):
            row = []
            for gx in range(size):
                row.append(Cell(x=gx, y=gy))
            self.grid.append(row)

        self.visited = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(False)
            self.visited.append(row)

        self._carve(0, 0)
        self._classify_and_build()
        return self.grid

    def _carve(self, gx, gy):
        self.visited[gy][gx] = True
        directions = list(_DELTA.keys())
        random.shuffle(directions)
        for d in directions:
            dx, dy = _DELTA[d]
            nx, ny = gx + dx, gy + dy
            size = self.size
            if 0 <= nx < size and 0 <= ny < size and not self.visited[ny][nx]:
                self.grid[gy][gx].walls[d] = False
                self.grid[ny][nx].walls[_OPPOSITE[d]] = False
                self._carve(nx, ny)

    def _classify_and_build(self):
        for gy in range(self.size):
            for gx in range(self.size):
                cell = self.grid[gy][gx]

                open_dirs = set()
                for d, blocked in cell.walls.items():
                    if not blocked:
                        open_dirs.add(d)
                count = len(open_dirs)

                if count == 1:
                    cell.cell_type = "dead_end"
                elif count == 2:
                    if open_dirs == {"north", "south"} or open_dirs == {"east", "west"}:
                        cell.cell_type = "corridor"
                    else:
                        cell.cell_type = "l_turn"
                elif count == 3:
                    cell.cell_type = "t_junction"
                else:
                    cell.cell_type = "plus"

                openings = {}
                for d, blocked in cell.walls.items():
                    openings[d] = not blocked

                self.playfield_map[(gx, gy)] = {
                    "type": cell.cell_type,
                    "openings": openings,
                }

    def get_playfield_map(self):
        return self.playfield_map
