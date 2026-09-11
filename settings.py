from pathlib import Path

import pygame

from gale import input_handler
from gale import frames

import pygame

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_p, "pause")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_KP_ENTER, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_d, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_a, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "jump")
input_handler.InputHandler.set_mouse_click_action(input_handler.MOUSE_BUTTON_1, "jump")


TITLE = "In the Trech on The Front"

input_handler


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Size we are trying to emulate
VIRTUAL_WIDTH = 1368
VIRTUAL_HEIGHT = 768


BASE_DIR = Path(__file__).parent

NUM_LEVELS = 1

TILEMAPS = {
    1: str(BASE_DIR / "assets" / "tilemaps" / "mapa1.json"),
    "map1": str(BASE_DIR / "assets" / "tilemaps" / "mapa1.json"),
    "level1": str(BASE_DIR / "assets" / "tilemaps" / "mapa1.json"),
}

TEXTURES = {
    "background": pygame.image.load(BASE_DIR / "assets" / "graphics" / "backgrounds" / "background_menu.jpeg"),
    "tiles": pygame.image.load(BASE_DIR / "assets" / "graphics" / "tileset.png"),
    "entitys": pygame.image.load(BASE_DIR / "assets" / "graphics" / "entitys.png"),
    "buildings": pygame.image.load(BASE_DIR / "assets" / "graphics" / "buildings.png"),
    
}

FRAMES = {
    "tiles": frames.generate_frames(TEXTURES["tiles"], 16, 16),
    "entitys": frames.generate_frames(TEXTURES["entitys"], 32, 32),
    "buildings": frames.generate_frames(TEXTURES["buildings"], 16, 16),
}

FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 8),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
}