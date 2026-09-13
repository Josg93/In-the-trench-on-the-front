from typing import Any, Dict

import pygame

from gale.tilemap import load_tiled_map
from gale.camera import Camera
from gale.timer import Timer

from src.definitions import Entitys, Buildings
from src.GameEntity import GameEntity
from src.Labourer import Labourer
from src.Soldier import Soldier
from src.GameBuilding import GameBuilding

import settings

class GameBattlefield():
    """
    Gestiona el campo de batalla, el mapa, los edificios, las entidades,
    la cámara y los recursos de comida (extracción de 10 de comida cada 10 segundos).
    """
    def __init__(self, map : Any = 1, camera : Camera = None) -> None:
        self.tilemap = load_tiled_map(settings.TILEMAPS[map])
        self.buildings = []
        self.entitys = []
        self.selected_entity = None
        
        # atributos de estadisticas de juego:
        self.food = 10000
        
        
        
        self.camera = camera
        self.collision_rects = []
        for obj in self.tilemap.object_layers.get("collission", []):
            self.collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        for obj in self.tilemap.object_layers.get("buildings", []):
            self.add_building(obj)

        for obj in self.tilemap.object_layers.get("entitys", []):
            self.add_entity(obj)

        
        
  
    def add_entity(self, obj: Any) -> None:
        entity_type = obj.type if obj.type else "Man"
        definition = None
        if entity_type in Entitys.LABOURERS:
            definition = Entitys.LABOURERS[entity_type].copy()
            self.entitys.append(
                Labourer(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height,
                    battlefield=self,
                    entity_type=entity_type,
                    **definition
                )
            )
            
        elif entity_type in Entitys.SOLDIERS:
            definition = Entitys.SOLDIERS[entity_type].copy()
            self.entitys.append(
                Soldier(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height,
                    battlefield=self,
                    entity_type=entity_type,
                    **definition
                )
            )
            
        else:
            definition = Entitys.LABOURERS.get("Man", {
                "texture_id": "entitys",
                "animations": {"idle": {"frames": [0], "interval": 0.1}}
            })
            self.entitys.append(
                Labourer(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height,
                    battlefield=self,
                    entity_type="Man",
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

        width = obj.width if obj.width > 0 else definition.pop("width")
        height = obj.height if obj.height > 0 else definition.pop("height")
        if "width" in definition:
            definition.pop("width")
        if "height" in definition:
            definition.pop("height")

        self.buildings.append(
            GameBuilding(
                obj.type,
                obj.x,
                obj.y,
                width,
                height,
                **definition
            )
        )
    def mouse_to_virtual(self, mouse_x : float , mouse_y : float ):
        virtual_mouse_x = mouse_x * (settings.VIRTUAL_WIDTH / settings.WINDOW_WIDTH)
        virtual_mouse_y = mouse_y * (settings.VIRTUAL_HEIGHT / settings.WINDOW_HEIGHT)
        return (virtual_mouse_x, virtual_mouse_y)
       
    def update(self, dt: float) -> None:
        for building in self.buildings:
            building.update(dt)

        #actualizar entidades
        for entity in self.entitys:
            entity.update(dt)

    def find_path(self, start_pos: tuple, goal_pos: tuple) -> list:
        from gale.ai.search import a_star

        start_r, start_c = self.tilemap.tile_at(start_pos[0], start_pos[1])
        goal_r, goal_c = self.tilemap.tile_at(goal_pos[0], goal_pos[1])

        if not self.tilemap.in_bounds(start_r, start_c) or not self.tilemap.in_bounds(goal_r, goal_c):
            return []

        def is_walkable(r, c):
            if not self.tilemap.in_bounds(r, c):
                return False
            
            # Verificar colisión con objetos de la capa 'collission'
            tx, ty = self.tilemap.position_of(r, c)
            tile_rect = pygame.Rect(tx, ty, self.tilemap.tile_width, self.tilemap.tile_height)
            for rect in self.collision_rects:
                if tile_rect.colliderect(rect):
                    return False

            

        def neighbors_fn(node):
            r, c = node
            neighbors = []
            directions = [
                (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
                (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414)
            ]
            for dr, dc, weight in directions:
                nr, nc = r + dr, c + dc
                if is_walkable(nr, nc):
                    neighbors.append(((nr, nc), weight))
            return neighbors

        def heuristic(n1, n2):
            return ((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2) ** 0.5

        if not is_walkable(goal_r, goal_c):
            return []

        tile_path = a_star((start_r, start_c), (goal_r, goal_c), neighbors_fn, heuristic)
        if not tile_path:
            return []

        waypoints = []
        for r, c in tile_path:
            tx, ty = self.tilemap.position_of(r, c)
            waypoints.append((tx + self.tilemap.tile_width / 2, ty + self.tilemap.tile_height / 2))
        return waypoints

    def on_input(self, input_id: str, input_data: Any) -> None:
        if hasattr(input_data, "pressed") and input_data.pressed:
            mouse_x, mouse_y = input_data.position
            virtual_mouse_x , virtual_mouse_y = self.mouse_to_virtual(mouse_x, mouse_y)
            world_x, world_y = self.camera.screen_to_world((virtual_mouse_x, virtual_mouse_y))

            #seleccionar entidad
            if input_id == "select_entity":
                clicked_entity = None
                for entity in self.entitys:
                    rect = entity.get_collision_rect()
                    if rect.collidepoint(world_x, world_y):
                        clicked_entity = entity
                        break

                for entity in self.entitys:
                    entity.selected = (entity == clicked_entity)
                self.selected_entity = clicked_entity


            elif input_id == "move_entity":
                if self.selected_entity is not None:
                    if hasattr(self.selected_entity, "stop_working"):
                        self.selected_entity.stop_working()

                    clicked_building = None
                    if getattr(self.selected_entity, "entity_type") in ["Man", "Woman"]:
                        for building in self.buildings:
                            if building.get_collision_rect().collidepoint(world_x, world_y):
                                clicked_building = building
                                break

                    if clicked_building is not None:
                        self.selected_entity.assigned_building = clicked_building
                        clicked_building.highlight()
                        b_rect = clicked_building.get_collision_rect()
                        target_x = b_rect.centerx
                        target_y = b_rect.centery
                        waypoints = self.find_path((self.selected_entity.x, self.selected_entity.y), (target_x, target_y))
                        if waypoints:
                            self.selected_entity.waypoints = waypoints
                            self.selected_entity.target_position = (target_x, target_y)
                        else:
                            self.selected_entity.waypoints = [(target_x, target_y)]
                            self.selected_entity.target_position = (target_x, target_y)
                    else:
                        entity_center = (self.selected_entity.x, self.selected_entity.y)
                        waypoints = self.find_path(entity_center, (world_x, world_y))
                        if waypoints:
                            self.selected_entity.waypoints = waypoints
                            self.selected_entity.target_position = (world_x, world_y)
                        else:
                            self.selected_entity.waypoints = [(world_x, world_y)]
                            self.selected_entity.target_position = (world_x, world_y)

    def render(self, surface: pygame.Surface) -> None:
        self.tilemap.render(surface, self.camera)
        for building in self.buildings:
            building.render(surface, self.camera)
        for entity in self.entitys:
            entity.render(surface, self.camera)
        