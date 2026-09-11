from typing import Any, Dict

import pygame

from gale.tilemap import load_tiled_map
from gale.camera import Camera

from src.definitions import Entitys
from src.GameEntity import GameEntity

import settings

class GameBattlefield():
    def __init__(self, map : Any = 1) -> None:
        self.tilemap = load_tiled_map(settings.TILEMAPS[map])
        self.buildings = []
        self.entitys = []
        self.items = []
        self.creatures = []

        self.camera = Camera(
            settings.VIRTUAL_WIDTH,
            settings.VIRTUAL_HEIGHT,
            x=self.tilemap.pixel_width / 2,
            y=self.tilemap.pixel_height / 2,
            bounds=pygame.Rect(0, 0, self.tilemap.pixel_width, self.tilemap.pixel_height)
        )

        for obj in self.tilemap.object_layers.get("entitys", []):
            self.add_entity(obj)

        
    def add_entity(self, obj: Any) -> None:
        entity_type = obj.type if obj.type else "Man"
        definition = None
        if entity_type in Entitys.LABOURERS:
            definition = Entitys.LABOURERS[entity_type]
        elif entity_type in Entitys.SOLDIERS:
            definition = Entitys.SOLDIERS[entity_type]
        else:
            definition = Entitys.LABOURERS.get("Man", {
                "texture_id": "entitys",
                "animations": {"idle": {"frames": [0], "interval": 0.1}}
            })

        self.entitys.append(
            GameEntity(
                obj.x,
                obj.y,
                obj.width,
                obj.height,
                **definition
            )
        )
   
    def update(self, dt: float) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        virtual_mouse_x = mouse_x * (settings.VIRTUAL_WIDTH / settings.WINDOW_WIDTH)
        virtual_mouse_y = mouse_y * (settings.VIRTUAL_HEIGHT / settings.WINDOW_HEIGHT)

        margin = 50
        scroll_speed = 500
        dx = 0
        dy = 0

        if virtual_mouse_x < margin:
            dx = -scroll_speed
        elif virtual_mouse_x > settings.VIRTUAL_WIDTH - margin:
            dx = scroll_speed

        if virtual_mouse_y < margin:
            dy = -scroll_speed
        elif virtual_mouse_y > settings.VIRTUAL_HEIGHT - margin:
            dy = scroll_speed

        self.camera.x += dx * dt
        self.camera.y += dy * dt
        self.camera.update(dt)

        for entity in self.entitys:
            entity.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.tilemap.render(surface, self.camera)
        for entity in self.entitys:
            entity.render(surface, self.camera)
        for creature in self.creatures:
            creature.render(surface, self.camera)
        for item in self.items:
            if item.active:
                item.render(surface, self.camera)
