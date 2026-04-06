import random
import py5

KEY_POOL = list("abcdefghijklmnopqrstuvwxyz0123456789")

_DEFAULTS = {
    "move_left": "a",
    "move_right": "d",
    "jump": "w",
}

_FIXED = {
    37: "rotate_clockwise",
    39: "rotate_counter_clockwise",
    27: "quit",
}


class Controls:
    def __init__(self):
        self.mapping = dict(_DEFAULTS)
        self.last_swap = None

    @staticmethod
    def get_key_id_from_py5():
        if py5.key != py5.CODED:
            return py5.key.lower()
        return py5.key_code

    def get_action(self, key_id):
        if isinstance(key_id, str):
            for action, key in self.mapping.items():
                if key == key_id:
                    return action
        elif isinstance(key_id, int) and key_id in _FIXED:
            return _FIXED[key_id]
        return None

    def rotate_world(self, direction):
        action = random.choice(list(self.mapping.keys()))

        pool = []
        for c in KEY_POOL:
            if c not in self.mapping.values():
                pool.append(c)

        new_key = random.choice(pool)
        old_key = self.mapping[action]
        self.mapping[action] = new_key
        self.last_swap = {"action": action, "old_key": old_key, "new_key": new_key}
        return self.last_swap

    def get_current_map(self):
        return dict(self.mapping)

    def is_held(self, action, keys_held):
        key = self.mapping.get(action)
        if key:
            return key in keys_held
        return False

    def reset(self):
        self.mapping = dict(_DEFAULTS)
        self.last_swap = None
