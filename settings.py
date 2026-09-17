from pathlib import Path

import pygame

from gale import input_handler
from gale import frames

import pygame

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_p, "pause")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_KP_ENTER, "enter")
input_handler.InputHandler.set_mouse_click_action(input_handler.MOUSE_BUTTON_1, "select_entity")
input_handler.InputHandler.set_mouse_click_action(input_handler.MOUSE_BUTTON_3, "move_entity")
input_handler.InputHandler.set_mouse_motion_action(None, "mouse_motion")


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
    "white1": pygame.image.load(BASE_DIR / "assets" / "graphics" / "backgrounds" / "white1.jpeg"),
    "white3": pygame.image.load(BASE_DIR / "assets" / "graphics" / "backgrounds" / "white3.jpeg"),
    "white_victory": pygame.image.load(BASE_DIR / "assets" / "graphics" / "backgrounds" / "white_victory.jpeg"),
    "red_victory": pygame.image.load(BASE_DIR / "assets" / "graphics" / "backgrounds" / "red_victory.jpeg"),
    
    "tiles": pygame.image.load(BASE_DIR / "assets" / "graphics" / "tileset.png"),
    
    "entitys": pygame.image.load(BASE_DIR / "assets" / "graphics" / "entitys.png"),
    
    "shooting": pygame.image.load(BASE_DIR / "assets" / "graphics" / "shooting.png"),
    
    "buildings": pygame.image.load(BASE_DIR / "assets" / "graphics" / "buildings.png"),
    "barracks": pygame.image.load(BASE_DIR / "assets" / "graphics" / "barracks.png"),
    "trench": pygame.image.load(BASE_DIR / "assets" / "graphics" / "trench.png"),
    "town1": pygame.image.load(BASE_DIR / "assets" / "graphics" / "town1.png"), 
    "house": pygame.image.load(BASE_DIR / "assets" / "graphics" / "house.png"), 
}

FRAMES = {
    "tiles": frames.generate_frames(TEXTURES["tiles"], 16, 16),
    "entitys": frames.generate_frames(TEXTURES["entitys"], 64,96),
    "shooting": frames.generate_frames(TEXTURES["shooting"], 120,96),
    "buildings": frames.generate_frames(TEXTURES["buildings"], 416, 320),
    "barracks": frames.generate_frames(TEXTURES["barracks"], 347, 321),
    "trench": frames.generate_frames(TEXTURES["trench"], 384, 672),
    "town1": frames.generate_frames(TEXTURES["town1"], 190, 596),
    "house": frames.generate_frames(TEXTURES["house"], 307, 245),
}

FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 8),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
    "big": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 32),
    "title": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 64),
}

SOUNDS ={
	
    
    "shoot1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "communist_shoot.mp3"),
    "shoot2": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "good_man_shoot.mp3"),
    "shoot3": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "shoot3.mp3"),
    "harvesting": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "harvesting.wav"),
}