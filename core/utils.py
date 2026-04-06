class Rect:
    def __init__(self, x, y, w, h):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)

    @property
    def width(self):
        return self.w

    @property
    def height(self):
        return self.h

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    @property
    def topleft(self):
        return (self.x, self.y)

    @topleft.setter
    def topleft(self, v):
        self.x = float(v[0])
        self.y = float(v[1])

    @property
    def centerx(self):
        return self.x + self.w / 2

    @property
    def centery(self):
        return self.y + self.h / 2

    @property
    def center(self):
        return (self.centerx, self.centery)

    def contains(self, px, py):
        in_x = self.x <= px <= self.x + self.w
        in_y = self.y <= py <= self.y + self.h
        return in_x and in_y

    def colliderect(self, other):
        horizontal_overlap = self.left < other.right and self.right > other.left
        vertical_overlap = self.top < other.bottom and self.bottom > other.top
        return horizontal_overlap and vertical_overlap
