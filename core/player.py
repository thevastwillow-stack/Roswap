import py5
from engine.collision import resolve
from core.constants import (
    flags,
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_MAX_HP, PLAYER_SPEED,
    JUMP_FORCE, GRAVITY, FALL_DAMAGE_THRESHOLD, FALL_DAMAGE_MULTIPLIER,
    COLORS,
)
from core.utils import Rect

_GRAVITY_VEC = {0: (0, GRAVITY), 90: (GRAVITY, 0), 180: (0, -GRAVITY), 270: (-GRAVITY, 0)}
_JUMP_VEC = {0: (0, -JUMP_FORCE), 90: (-JUMP_FORCE, 0), 180: (0, JUMP_FORCE), 270: (JUMP_FORCE, 0)}


class Player:

    def __init__(self, x, y):
        self.rect = Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False
        self.rotation = 0
        self.hp = float(PLAYER_MAX_HP)

    def rotate(self, direction):
        if direction == "clockwise":
            self.rotation = (self.rotation + 90) % 360
        else:
            self.rotation = (self.rotation - 90) % 360
        self.vel_x = 0.0
        self.vel_y = 0.0

    def move(self, direction):
        if direction == "right":
            speed = PLAYER_SPEED
        else:
            speed = -PLAYER_SPEED

        if self.rotation in (0, 180):
            if self.rotation == 0:
                self.vel_x = speed
            else:
                self.vel_x = -speed
        else:
            if self.rotation == 90:
                self.vel_y = speed
            else:
                self.vel_y = -speed

    def jump(self):
        if not self.on_ground:
            return
        jx, jy = _JUMP_VEC[self.rotation]
        self.vel_x = jx
        self.vel_y = jy

    def update(self, dt, platforms):
        gx, gy = _GRAVITY_VEC[self.rotation]
        self.vel_x += gx * dt
        self.vel_y += gy * dt

        MAX_VEL = 1200.0
        if self.vel_x < -MAX_VEL:
            self.vel_x = -MAX_VEL
        elif self.vel_x > MAX_VEL:
            self.vel_x = MAX_VEL

        if self.vel_y < -MAX_VEL:
            self.vel_y = -MAX_VEL
        elif self.vel_y > MAX_VEL:
            self.vel_y = MAX_VEL

        if self.rotation in (90, 270):
            pre_speed = abs(self.vel_x)
        else:
            pre_speed = abs(self.vel_y)

        was_ground = self.on_ground
        self.vel_x, self.vel_y, self.on_ground = resolve(
            self.rect, self.vel_x, self.vel_y, self.rotation, platforms, dt
        )

        if not was_ground and self.on_ground:
            if not flags["no_damage"] and pre_speed > FALL_DAMAGE_THRESHOLD:
                damage = (pre_speed - FALL_DAMAGE_THRESHOLD) * FALL_DAMAGE_MULTIPLIER
                new_hp = self.hp - damage
                if new_hp < 0.0:
                    new_hp = 0.0
                self.hp = new_hp

    def draw(self):
        py5.fill(*COLORS["player"])
        py5.no_stroke()
        py5.rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

    def get_rect(self):
        return self.rect

    def is_dead(self):
        return self.hp <= 0
