from typing import Any, Dict

import pygame

from gale.tilemap import load_tiled_map
from gale.camera import Camera

from src.definitions import Entitys, Buildings
from src.GameEntity import GameEntity
from src.GameBuilding import GameBuilding

import settings

class GameBattlefield():
    def __init__(self, map : Any = 1) -> None:
        self.tilemap = load_tiled_map(settings.TILEMAPS[map])
        self.buildings = []
        self.entitys = []
        self.items = []
        self.creatures = []
        self.selected_entity = None

        self.camera = Camera(
            settings.VIRTUAL_WIDTH,
            settings.VIRTUAL_HEIGHT,
            x=0,
            y=self.tilemap.pixel_height,
            bounds=pygame.Rect(0, 0, self.tilemap.pixel_width, self.tilemap.pixel_height)
        )

        for obj in self.tilemap.object_layers.get("entitys", []):
            self.add_entity(obj)

        for obj in self.tilemap.object_layers.get("buildings", []):
            self.add_building(obj)

        
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

    def add_building(self, obj: Any) -> None:
        b_type = obj.type if obj.type else "mill"
        definition = None
        if b_type in Buildings.CIVIL_BUILDINGS:
            definition = Buildings.CIVIL_BUILDINGS[b_type].copy()
        elif b_type in Buildings.MILITARY_BUILDINGS:
            definition = Buildings.MILITARY_BUILDINGS[b_type].copy()
        else:
            definition = Buildings.CIVIL_BUILDINGS["mill"].copy()

        width = obj.width if obj.width > 0 else definition.pop("width", 416)
        height = obj.height if obj.height > 0 else definition.pop("height", 320)
        if "width" in definition:
            definition.pop("width")
        if "height" in definition:
            definition.pop("height")

        self.buildings.append(
            GameBuilding(
                obj.x,
                obj.y,
                width,
                height,
                **definition
            )
        )
   
    def update(self, dt: float) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        virtual_mouse_x = mouse_x * (settings.VIRTUAL_WIDTH / settings.WINDOW_WIDTH)
        virtual_mouse_y = mouse_y * (settings.VIRTUAL_HEIGHT / settings.WINDOW_HEIGHT)

        margin = 50
        scroll_speed = 1000
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

    def on_input(self, input_id: str, input_data: Any) -> None:
        if hasattr(input_data, "pressed") and input_data.pressed:
            mouse_x, mouse_y = input_data.position
            virtual_mouse_x = mouse_x * (settings.VIRTUAL_WIDTH / settings.WINDOW_WIDTH)
            virtual_mouse_y = mouse_y * (settings.VIRTUAL_HEIGHT / settings.WINDOW_HEIGHT)
            world_x, world_y = self.camera.screen_to_world((virtual_mouse_x, virtual_mouse_y))

            if input_id == "select_entity":
                clicked_entity = None
                for entity in self.entitys:
                    rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
                    if rect.collidepoint(world_x, world_y):
                        clicked_entity = entity
                        break

                for entity in self.entitys:
                    entity.selected = (entity == clicked_entity)
                self.selected_entity = clicked_entity

            elif input_id == "move_entity":
                if self.selected_entity is not None:
                    self.selected_entity.target_position = (world_x, world_y)

    def render(self, surface: pygame.Surface) -> None:
        self.tilemap.render(surface, self.camera)
        for building in self.buildings:
            building.render(surface, self.camera)
        for entity in self.entitys:
            entity.render(surface, self.camera)
        for creature in self.creatures:
            creature.render(surface, self.camera)
        for item in self.items:
            if item.active:
                item.render(surface, self.camera)

