import random
import importlib
from pathlib import Path

_registry = {}

_rooms_dir = Path(__file__).parent

for _py_file in sorted(_rooms_dir.rglob("*.py")):
    if _py_file.name.startswith("_"):
        continue
    _rel = _py_file.relative_to(_rooms_dir)
    _module_name = "rooms." + ".".join(_rel.with_suffix("").parts)
    try:
        _mod = importlib.import_module(_module_name)
    except ImportError as exc:
        print(f"[rooms] Warning: could not import {_module_name!r}: {exc}")
        continue
    for _cls in getattr(_mod, "VARIANTS", []):
        if _cls.ROOM_TYPE not in _registry:
            _registry[_cls.ROOM_TYPE] = []
        _registry[_cls.ROOM_TYPE].append(_cls)


def get_room(room_type):
    pool = _registry.get(room_type)
    if not pool:
        raise KeyError(f"{room_type!r} — available: {sorted(_registry)}")
    return random.choice(pool)
