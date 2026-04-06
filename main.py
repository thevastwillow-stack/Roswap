import os

if 'JAVA_HOME' not in os.environ:
    print("Warning: JAVA_HOME not set")
    exit()

import py5
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLORS, flags
from core.player import Player
from engine.camera import Camera
from engine.controls import Controls
from ui.hud import HUD
from ui.menu import Menu
from maze.generator import MazeGenerator, find_neighbour
from rooms.registry import get_room

game_state = 'MENU'

playfield_map = None
rooms = {}
start_anchor = None
end_anchor = None
current_anchor = None
current_room = None

player = None
controls = None
camera = None
hud = None
menu = None

keys_held = set()
last_time = 0


def setup():
    py5.size(SCREEN_WIDTH, SCREEN_HEIGHT)
    py5.frame_rate(FPS)
    global menu, hud, controls, camera
    menu = Menu()
    hud = HUD()
    controls = Controls()
    camera = Camera()


def draw():
    global last_time
    current_time = py5.millis()
    dt = (current_time - last_time) / 1000.0
    last_time = current_time

    if game_state == 'MENU':
        menu.draw()
    elif game_state == 'PLAYING':
        _update_playing(dt)
        _draw_playing()
    elif game_state == 'WIN':
        _draw_end_screen('YOU WIN', (255, 255, 255))
    elif game_state == 'DEAD':
        _draw_end_screen('YOU DIED', (200, 50, 50))


def _update_playing(dt):
    global game_state

    if controls.is_held('move_left', keys_held):
        player.move('left')
    if controls.is_held('move_right', keys_held):
        player.move('right')

    player.update(dt, current_room.get_platforms())
    camera.set_rotation(player.rotation)
    hud.update(dt)

    if player.is_dead():
        game_state = 'DEAD'
        return

    exit_dir = current_room.check_exit(player.get_rect())
    if exit_dir:
        next_anchor = find_neighbour(current_anchor, exit_dir, playfield_map)
        if next_anchor is None or next_anchor not in rooms:
            return
        if next_anchor == end_anchor:
            game_state = 'WIN'
        else:
            _enter_room(next_anchor, exit_dir)


def _draw_playing():
    camera.begin_draw()
    current_room.draw()
    player.draw()
    camera.end_draw()
    hud.draw(controls.get_current_map(), player.hp)


def _enter_room(next_anchor, exit_dir):
    global current_anchor, current_room

    if exit_dir == 'north':
        entry_dir = 'south'
    elif exit_dir == 'south':
        entry_dir = 'north'
    elif exit_dir == 'east':
        entry_dir = 'west'
    else:
        entry_dir = 'east'

    current_anchor = next_anchor
    current_room = rooms[next_anchor]
    player.rect.topleft = current_room.spawn_point(entry_dir)


def _start_game(difficulty):
    global playfield_map, rooms, start_anchor, end_anchor
    global current_anchor, current_room, player, game_state

    maze_gen = MazeGenerator(difficulty)
    maze_gen.generate()
    playfield_map = maze_gen.get_playfield_map()

    rooms = {}
    for anchor, entry in playfield_map.items():
        try:
            cls = get_room(entry['type'])
            rooms[anchor] = cls(entry['openings'])
        except KeyError as e:
            print(f'Warning — no room for {e}. Skipping.')

    size = maze_gen.size
    start_anchor = (0, 0)
    end_anchor = (size - 1, size - 1)
    current_anchor = start_anchor
    current_room = rooms[current_anchor]
    player = Player(*current_room.spawn_point('none'))
    camera.set_rotation(0)
    game_state = 'PLAYING'


def key_pressed():
    kid = Controls.get_key_id_from_py5()
    keys_held.add(kid)

    if game_state == 'MENU':
        if isinstance(kid, str):
            menu.handle_key(kid)
    elif game_state == 'PLAYING':
        action = controls.get_action(kid)
        if action == 'jump':
            player.jump()
        elif action == 'rotate_clockwise':
            player.rotate('clockwise')
            if not flags["no_swap"]:
                swap = controls.rotate_world('clockwise')
                hud.notify_swap(swap)
        elif action == 'rotate_counter_clockwise':
            player.rotate('counter_clockwise')
            if not flags["no_swap"]:
                swap = controls.rotate_world('counter_clockwise')
                hud.notify_swap(swap)
        elif action == 'quit':
            py5.exit_sketch()
    elif game_state in ('WIN', 'DEAD'):
        _restart()


def key_released():
    keys_held.discard(Controls.get_key_id_from_py5())


def mouse_pressed():
    if game_state == 'MENU':
        menu.handle_click(py5.mouse_x, py5.mouse_y)
        if menu.is_selected():
            _start_game(menu.get_selected())


def _draw_end_screen(message, color):
    py5.background(*COLORS['background'])
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.fill(*color)
    py5.text_size(64)
    py5.text(message, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)
    py5.fill(*COLORS['hud_text'])
    py5.text_size(22)
    py5.text('press any key to play again', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)


def _restart():
    global game_state, menu
    game_state = 'MENU'
    menu = Menu()
    controls.reset()


py5.run_sketch()
