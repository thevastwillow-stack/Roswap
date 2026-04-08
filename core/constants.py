SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
FPS = 60

WALL = 60
GAP = 120
GAP_START = (SCREEN_WIDTH - GAP) // 2
GAP_END = GAP_START + GAP

DIFFICULTY_GRID = {"easy": 7, "medium": 13, "hard": 17}

GRAVITY = 800
PLAYER_SPEED = 220
JUMP_FORCE = 400
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_MAX_HP = 100
FALL_DAMAGE_THRESHOLD = 750
FALL_DAMAGE_MULTIPLIER = 0.075
MAX_VEL = 1200

HUD_FLASH_DURATION = 2.0

COLORS = {
    "background": (30, 30, 30),
    "player": (220, 220, 220),
    "platform": (100, 100, 100),
    "hud_text": (255, 255, 255),
    "hud_flash": (255, 220, 0),
    "exit_zone": (0, 180, 0),
    "hp_bar": (200, 50, 50),
    "hp_bar_bg": (60, 60, 60),
}

flags = {
    "unlocked": False,
    "no_damage": False,
    "no_swap": False,
}
