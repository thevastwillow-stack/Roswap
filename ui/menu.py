import py5
from core.constants import flags, SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, DIFFICULTY_GRID
from core.utils import Rect

_PI_SEQ = "3141592653"

_DIFFICULTIES = [
    (key, f"{key.capitalize()} — {size}×{size}")
    for key, size in DIFFICULTY_GRID.items()
]

_BTN_W = 320
_BTN_H = 60
_BTN_GAP = 20
_BTN_FIRST_Y = 260
_DBG_BTN_W = 200
_DBG_BTN_H = 36
_DBG_BTN_GAP = 10
_DBG_MARGIN = 16
_DBG_LABELS = [("no_damage", "No Damage"), ("no_swap", "No Key Swap")]


class Menu:
    def __init__(self):
        self.selected = None
        self.hovered = None
        self._buttons = []
        self._dbg_buttons = []
        self._pi_progress = 0
        self._build_buttons()
        self._build_dbg_buttons()

    def draw(self):
        py5.background(*COLORS["background"])
        py5.no_stroke()

        py5.text_size(72)
        py5.text_align(py5.CENTER)
        py5.fill(255, 255, 255)
        py5.text("ROSWAP", SCREEN_WIDTH / 2, 110)

        py5.text_size(20)
        py5.fill(180, 180, 180)
        py5.text("rotate the world. lose your keys.", SCREEN_WIDTH / 2, 175)

        mx = py5.mouse_x
        my = py5.mouse_y
        self.hovered = None

        for btn in self._buttons:
            rect = btn["rect"]
            is_hov = rect.contains(mx, my)
            py5.no_stroke()
            if is_hov:
                self.hovered = btn["key"]
                py5.fill(80, 80, 80)
            else:
                py5.fill(50, 50, 50)
            py5.rect(rect.x, rect.y, rect.w, rect.h, 6)
            py5.text_size(24)
            py5.text_align(py5.CENTER)
            py5.fill(255, 255, 255)
            py5.text(btn["label"], rect.x + rect.w / 2, rect.y + rect.h / 2 + 9)

        if flags["unlocked"]:
            bx = SCREEN_WIDTH - _DBG_BTN_W - _DBG_MARGIN
            py5.text_size(14)
            py5.text_align(py5.CENTER)
            py5.fill(120, 120, 120)
            py5.no_stroke()
            py5.text("DEBUG", bx + _DBG_BTN_W / 2, _DBG_MARGIN - 2)
            for btn in self._dbg_buttons:
                rect = btn["rect"]
                active = flags[btn["flag"]]
                hovered = rect.contains(mx, my)
                if active:
                    bg = (40, 160, 80)
                elif hovered:
                    bg = (70, 70, 70)
                else:
                    bg = (40, 40, 40)
                py5.no_stroke()
                py5.fill(*bg)
                py5.rect(rect.x, rect.y, rect.w, rect.h, 4)
                if active:
                    py5.fill(255)
                else:
                    py5.fill(100)
                py5.ellipse(rect.x + 16, rect.y + rect.h / 2, 10, 10)
                py5.fill(255)
                py5.text_align(py5.LEFT)
                py5.text(btn["label"], rect.x + 26, rect.y + rect.h / 2 + 5)

    def handle_key(self, char):
        if flags["unlocked"]:
            return
        expected = _PI_SEQ[self._pi_progress]
        if char == expected:
            self._pi_progress += 1
            if self._pi_progress == len(_PI_SEQ):
                flags["unlocked"] = True
                self._pi_progress = 0
        else:
            if char == _PI_SEQ[0]:
                self._pi_progress = 1
            else:
                self._pi_progress = 0

    def handle_click(self, mx, my):
        if flags["unlocked"]:
            for btn in self._dbg_buttons:
                if btn["rect"].contains(mx, my):
                    flags[btn["flag"]] = not flags[btn["flag"]]
                    return
        for btn in self._buttons:
            if btn["rect"].contains(mx, my):
                self.selected = btn["key"]
                break

    def is_selected(self):
        return self.selected is not None

    def get_selected(self):
        return self.selected

    def _build_buttons(self):
        self._buttons.clear()
        btn_x = SCREEN_WIDTH / 2 - _BTN_W / 2
        for i, (key, label) in enumerate(_DIFFICULTIES):
            btn_y = _BTN_FIRST_Y + i * (_BTN_H + _BTN_GAP)
            self._buttons.append({
                "key": key,
                "label": label,
                "rect": Rect(btn_x, btn_y, _BTN_W, _BTN_H),
            })

    def _build_dbg_buttons(self):
        self._dbg_buttons.clear()
        bx = SCREEN_WIDTH - _DBG_BTN_W - _DBG_MARGIN
        for i, (flag, label) in enumerate(_DBG_LABELS):
            by = _DBG_MARGIN + i * (_DBG_BTN_H + _DBG_BTN_GAP)
            self._dbg_buttons.append({
                "flag": flag,
                "label": label,
                "rect": Rect(bx, by, _DBG_BTN_W, _DBG_BTN_H),
            })
