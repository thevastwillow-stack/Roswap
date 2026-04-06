import py5
from core.constants import SCREEN_WIDTH, HUD_FLASH_DURATION, COLORS, PLAYER_MAX_HP

_X_ANCHOR = SCREEN_WIDTH - 16
_LINE_H = 26
_PAD_X = 10
_PAD_Y = 8
_BAR_W = 130
_BAR_H = 11


class HUD:
    def __init__(self):
        self.flash_timer = 0.0
        self.last_swap = None

    def notify_swap(self, swap):
        self.last_swap = swap
        self.flash_timer = HUD_FLASH_DURATION

    def update(self, dt):
        self.flash_timer = self.flash_timer - dt
        if self.flash_timer < 0.0:
            self.flash_timer = 0.0

    def draw(self, key_map, player_hp):
        move_left = key_map.get("move_left", "?").upper()
        move_right = key_map.get("move_right", "?").upper()
        jump = key_map.get("jump", "?").upper()

        text_lines = [
            (f"\u2190 {move_left}  \u2192 {move_right}  JUMP {jump}", COLORS["hud_text"]),
        ]
        if self.flash_timer > 0 and self.last_swap:
            action = self.last_swap.get("action", "?")
            new_key = self.last_swap.get("new_key", "?").upper()
            text_lines.append((f"SWAPPED: {action} \u2192 {new_key}", COLORS["hud_flash"]))

        py5.text_size(18)

        # Width: widest of text lines vs HP bar row ("HP " + bar + " 000")
        max_text_w = max(py5.text_width(t) for t, _ in text_lines)
        py5.text_size(14)
        hp_label_w = py5.text_width("HP ")
        hp_num_w = py5.text_width(" 100")
        hp_row_w = hp_label_w + _BAR_W + hp_num_w
        box_content_w = max(max_text_w, hp_row_w)

        box_w = box_content_w + _PAD_X * 2
        hp_row_h = _BAR_H + 10          # a little breathing room below bar
        box_h = _PAD_Y + hp_row_h + len(text_lines) * _LINE_H + _PAD_Y
        box_x = _X_ANCHOR - box_w
        box_y = 16

        # Background
        py5.no_stroke()
        py5.fill(0, 0, 0, 160)
        py5.rect(box_x - _PAD_X, box_y - _PAD_Y, box_w + _PAD_X, box_h, 4)

        # ── HP bar ──────────────────────────────────────────────
        hp_frac = max(0.0, min(1.0, player_hp / PLAYER_MAX_HP))
        bar_row_y = box_y + _PAD_Y
        bar_x = box_x + hp_label_w

        # "HP" label
        py5.text_size(14)
        py5.text_align(py5.LEFT)
        py5.fill(*COLORS["hud_text"])
        py5.text("HP", box_x, bar_row_y + _BAR_H - 1)

        # Bar track
        py5.fill(*COLORS["hp_bar_bg"])
        py5.rect(bar_x, bar_row_y, _BAR_W, _BAR_H, 3)

        # Bar fill — shifts to orange then bright red as HP drops
        if hp_frac > 0.5:
            bar_color = COLORS["hp_bar"]
        elif hp_frac > 0.25:
            bar_color = (220, 140, 20)
        else:
            bar_color = (230, 40, 40)
        if hp_frac > 0:
            py5.fill(*bar_color)
            py5.rect(bar_x, bar_row_y, _BAR_W * hp_frac, _BAR_H, 3)

        # Numeric value
        py5.fill(*COLORS["hud_text"])
        py5.text_size(14)
        py5.text_align(py5.LEFT)
        py5.text(str(int(player_hp)), bar_x + _BAR_W + 4, bar_row_y + _BAR_H - 1)

        # ── Key binding lines ────────────────────────────────────
        py5.text_align(py5.RIGHT)
        for i, (text, color) in enumerate(text_lines):
            py5.fill(*color)
            py5.text_size(18)
            line_y = box_y + _PAD_Y + hp_row_h + i * _LINE_H + _LINE_H - 6
            py5.text(text, _X_ANCHOR, line_y)
