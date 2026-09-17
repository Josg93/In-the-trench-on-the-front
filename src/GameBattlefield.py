from src.trench import Trench
from typing import Any, Dict

import pygame

from gale.tilemap import load_tiled_map
from gale.camera import Camera
from gale.timer import Timer
from gale.ai.graph import Graph
from gale.ai.search import a_star
from gale.ai.formation import LineFormation

from src.definitions import Entitys, Buildings
from src.GameEntity import GameEntity
from src.Labourer import Labourer
from src.Soldier import Soldier
from src.GameBuilding import GameBuilding
import random

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
        self.is_dragging = False
        self.drag_start = (0, 0)
        self.drag_end = (0, 0)
        
        # atributos de estadisticas de juego:
        self.food = 1000
        
        
        self.camera = camera
        self.collision_rects = []
        for obj in self.tilemap.object_layers.get("collission", []):
            self.collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        
        for obj in self.tilemap.object_layers.get("buildings", []):
            self.add_building(obj)
            

        self.build_graph()
        
 
        
        for obj in self.tilemap.object_layers.get("entitys", []):
            self.add_entity(obj)

        
    
    # === Construcción del Grafo de Navegación para la capa ground ===
    def build_graph(self) -> None:
        # Dimensiones de la capa ground (píxeles): x en [0, 16000], y en [608, 1184]
        # Tamaño de tile: 32x32 (deducido de la configuración y el código existente)
        TILE_W = self.tilemap.tile_width
        TILE_H = self.tilemap.tile_height
        GROUND_X0, GROUND_Y0 = 0, 608
        GROUND_X1, GROUND_Y1 = 16000, 1184



        # Índices de celda (row, col) que delimitan la capa ground:
        # - Fila (row): py / 32. 608 / 32 = 19, 1184 / 32 = 37  -> rows 19 .. 36 (18 filas)
        # - Columna (col): px / 32. 0 / 32 = 0, 16000 / 32 = 500 -> cols 0 .. 499 (500 columnas)
        self.ground_start_row = GROUND_Y0 // TILE_H      # 19
        self.ground_end_row   = GROUND_Y1 // TILE_H      # 37 (exclusive)
        self.ground_start_col = 0
        self.ground_end_col   = GROUND_X1 // TILE_W      # 500 (exclusive)

        # Instanciamos el grafo de navegación de Gale (estructura _adjacency: Dict[T, Dict[T, float]])
        self.nav_graph = Graph()

        # Función auxiliar: devuelve el rectángulo del tile en píxeles dada su fila y columna
        def tile_rect(r: int, c: int) -> pygame.Rect:
            tx, ty = self.tilemap.position_of(r, c)
            return pygame.Rect(tx, ty, TILE_W, TILE_H)

        #Poblamos el grafo: añadimos nodos solo para tiles válidos (no bloqueados por colisiones)
        for r in range(self.ground_start_row, self.ground_end_row):
            for c in range(self.ground_start_col, self.ground_end_col):
                tr = tile_rect(r, c)
                blocked = False
                # Colisionar con rectángulos de la capa "collission" (obstáculos estáticos)
                for rect in self.collision_rects:
                    if tr.colliderect(rect):
                        blocked = True
                        break
                # Colisionar con edificios sólidos (si tienen collidable=True y rect de colisión)
                if not blocked:
                    for building in self.buildings:
                        if getattr(building, "collidable", False):
                            br = building.get_collision_rect()
                            if tr.colliderect(br):
                                blocked = True
                                break
                # Si el tile no está bloqueado, lo añadimos como nodo aislado en el grafo
                if not blocked:
                    self.nav_graph._adjacency[(r, c)] = {}

        # Conectamos nodos con vecinos en 8 direcciones (ortogonales y diagonales)
        # Pesos: 1.0 para movimiento horizontal/vertical, 1.414 ≈ sqrt(2) para diagonal
        WEIGHT_ORTH = 1.0
        WEIGHT_DIAG = 1.414
        
        for r in range(self.ground_start_row, self.ground_end_row):
            for c in range(self.ground_start_col, self.ground_end_col):
                node = (r, c)
                if node not in self.nav_graph._adjacency:
                    continue  # nodo bloqueado, saltar
                # Explorar los 8 vecinos posibles
                for dr, dc, w in [
                    (-1, 0, WEIGHT_ORTH), (1, 0, WEIGHT_ORTH),
                    (0, -1, WEIGHT_ORTH), (0, 1, WEIGHT_ORTH),
                    (-1, -1, WEIGHT_DIAG), (-1, 1, WEIGHT_DIAG),
                    (1, -1, WEIGHT_DIAG), (1, 1, WEIGHT_DIAG)
                ]:
                    nr, nc = r + dr, c + dc
                    # Verificar que el vecino esté dentro de los límites de la capa ground
                    if self.ground_start_row <= nr < self.ground_end_row and self.ground_start_col <= nc < self.ground_end_col:
                        neighbor = (nr, nc)
                        if neighbor in self.nav_graph._adjacency:
                            # Añadimos la arista en ambos sentidos (grafo efectivamente no dirigido para el movimiento)
                            self.nav_graph._adjacency[node][neighbor] = w
                            self.nav_graph._adjacency[neighbor][node] = w

        # === Fin construcción grafo ===
        
    def find_path(self, start_pos: tuple, goal_pos: tuple) -> list:
        """
        Busca el camino más corto entre start_pos y goal_pos usando A* sobre el grafo de navegación
        preconstruido para la capa ground. Devuelve una lista de waypoints en coordenadas de píxel
        (centros de los tiles) que la entidad debe seguir.
        
        El grafo está restringido a la capa ground (rows 19..36, cols 0..499) y los nodos bloqueados
        por colisiones o edificios han sido eliminados previamente.
        """
        # Convertir posiciones de mundo a coordenadas de tile (fila, columna)
        start_r, start_c = self.tilemap.tile_at(start_pos[0], start_pos[1])
        goal_r, goal_c = self.tilemap.tile_at(goal_pos[0], goal_pos[1])

        # 1. Verificar que tanto el inicio como el objetivo estén dentro de los límites
        #    de la capa ground (usamos los atributos instalados en __init__)
        if not (self.ground_start_row <= start_r < self.ground_end_row and self.ground_start_col <= start_c < self.ground_end_col):
            return []
        if not (self.ground_start_row <= goal_r < self.ground_end_row and self.ground_start_col <= goal_c < self.ground_end_col):
            return []

        # 2. Verificar que ambos nodos existan en el grafo (no estén bloqueados por obstáculos)
        if (start_r, start_c) not in self.nav_graph._adjacency:
            return []
        if (goal_r, goal_c) not in self.nav_graph._adjacency:
            return []

        # 3. Ejecutar A* usando el grafo de Gale
        #    a_star(start, goal, graph_or_fn, heuristic) acepta un objeto Graph y una función heurística
        tile_path = a_star((start_r, start_c), (goal_r, goal_c), self.nav_graph, self._heuristic)
        
        if not tile_path:
            return []

        # 4. Convertir la ruta de nodos (fila, columna) a waypoints en píxeles
        #    (centro de cada tile) para entregárselos a la entidad
        waypoints = []
        tw = self.tilemap.tile_width
        th = self.tilemap.tile_height
        for r, c in tile_path:
            tx, ty = self.tilemap.position_of(r, c)
            # Centro del tile: sumamos la mitad del ancho/alto
            waypoints.append((tx + tw / 2, ty + th / 2))
        return waypoints

    def _heuristic(self, n1: tuple, n2: tuple) -> float:
        """
        Heurística euclidiana entre dos nodos (fila, columna).
        Usa la fórmula sqrt((r1-r2)^2 + (c1-c2)^2).
        """
        r1, c1 = n1
        r2, c2 = n2
        return ((r1 - r2) ** 2 + (c1 - c2) ** 2) ** 0.5




    

    def add_entity(self, obj: Any) -> None:
        entity_type = obj.type if obj.type else "Man"
        definition = None
        if entity_type in Entitys.LABOURERS:
            definition = Entitys.LABOURERS[entity_type].copy()
            target_y = random.randint(700,900)
            birth_way = self.find_path((obj.x, obj.y), (417, target_y))
            self.entitys.append(
                Labourer(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height,
                    battlefield=self,
                    entity_type=entity_type,
                    waypoints = birth_way, 
                    target_position = (417,862),
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
                    waypoints = self.find_path((obj.x, obj.y), (417, 862)),
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

        width = definition.pop("width")
        height = definition.pop("height")
        
        if obj.type == "trench":
            building_obj = Trench(
                obj.type, obj.x, obj.y, width, height, **definition
            )
        else:
            building_obj = GameBuilding(
                obj.type, obj.x, obj.y, width, height, **definition
            )
        self.buildings.append(building_obj)
        if obj.type == "town" :
            self.capitol = self.buildings[-1]
        
        
    # ----------------- UTILITIES -----------------        
    def mouse_to_virtual(self, mouse_x : float , mouse_y : float ):
        virtual_mouse_x = mouse_x * (settings.VIRTUAL_WIDTH / settings.WINDOW_WIDTH)
        virtual_mouse_y = mouse_y * (settings.VIRTUAL_HEIGHT / settings.WINDOW_HEIGHT)
        return (virtual_mouse_x, virtual_mouse_y)
       
    def get_distance(self, target_x, target_y, entity=None):   
        target_entity = entity if entity is not None else self.selected_entity
        if target_entity is not None and hasattr(target_entity, "x"):
            entity_center_x = target_entity.x + target_entity.width / 2
            entity_center_y = target_entity.y + target_entity.height / 2
            dx = target_x - entity_center_x
            dy = target_y - entity_center_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            return distance
        return float('inf')
     
    # -----------------------------------------------   
    def update(self, dt: float) -> None:
        for building in self.buildings:
            building.update(dt)

        #actualizar entidades
        for entity in self.entitys:
            entity.update(dt)
       
        # Liberar espacios en edificios/trincheras si la entidad muere
        for entity in self.entitys:
            if entity.hp <= 0:
                if hasattr(entity, "stop_working"):
                    entity.stop_working()

        self.entitys = [e for e in self.entitys if getattr(e, "hp", 100) > 0]
        previous_building_count = len(self.buildings)
        self.buildings = [e for e in self.buildings if getattr(e, "hp", 100) > 0]
        if len(self.buildings) < previous_building_count:
            self.build_graph()




    def on_input(self, input_id: str, input_data: Any) -> None:
        # Verificar que el evento contenga una posición de ratón antes de procesarlo
        if not hasattr(input_data, "position"):
            return

        if input_id == "mouse_motion" and self.is_dragging:
            mouse_x, mouse_y = input_data.position
            virtual_mouse_x, virtual_mouse_y = self.mouse_to_virtual(mouse_x, mouse_y)
            world_x, world_y = self.camera.screen_to_world((virtual_mouse_x, virtual_mouse_y))
            self.drag_end = (world_x, world_y)

        if hasattr(input_data, "pressed"):
            mouse_x, mouse_y = input_data.position
            virtual_mouse_x , virtual_mouse_y = self.mouse_to_virtual(mouse_x, mouse_y)
            world_x, world_y = self.camera.screen_to_world((virtual_mouse_x, virtual_mouse_y))

            #seleccionar entidad con click o drag (box selection)
            if input_id == "select_entity":
                if input_data.pressed:
                    self.drag_start = (world_x, world_y)
                    self.drag_end = (world_x, world_y)
                    self.is_dragging = True
                else:
                    if self.is_dragging:
                        self.drag_end = (world_x, world_y)
                        dx = self.drag_end[0] - self.drag_start[0]
                        dy = self.drag_end[1] - self.drag_start[1]
                        dist = (dx**2 + dy**2)**0.5

                        if dist > 8:
                            # Selección por rectángulo (Drag Box Select - añade a la selección)
                            x1, y1 = self.drag_start
                            x2, y2 = self.drag_end
                            box_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

                            for entity in self.entitys:
                                if not entity.is_enemy:
                                    rect = entity.get_selection_rect() if hasattr(entity, "get_selection_rect") else entity.get_collision_rect()
                                    if box_rect.colliderect(rect):
                                        entity.selected = True
                        else:
                            # Selección individual por clic simple
                            clicked_entity = None
                            for entity in self.entitys:
                                rect = entity.get_selection_rect() if hasattr(entity, "get_selection_rect") else entity.get_collision_rect()
                                if rect.collidepoint(world_x, world_y) and entity.is_enemy is False :
                                    clicked_entity = entity
                                    break

                            for entity in self.entitys:
                                entity.selected = (entity == clicked_entity)
                            self.selected_entity = clicked_entity

                        self.is_dragging = False

            
            elif input_id == "move_entity":
                selected_units = [e for e in self.entitys if getattr(e, "selected", False) and not getattr(e, "is_enemy", False)]
                if not selected_units and self.selected_entity is not None:
                    selected_units = [self.selected_entity]

                if selected_units:
                    # Si hay un grupo seleccionado (> 1 unidad), usar formación LineFormation de Gale
                    if len(selected_units) > 1:
                        formation = LineFormation(spacing=48)
                        for i, unit in enumerate(selected_units):
                            offset = formation.slot_offset(i, len(selected_units))
                            slot_x = world_x + offset.x
                            slot_y = world_y + offset.y

                            if getattr(unit, "entity_type", None) in ["Soldier", "Machine"] and getattr(unit, "assigned_building", None) is not None:
                                if hasattr(unit, "un_trench"):
                                    unit.un_trench((slot_x, slot_y))
                            else:
                                entity_center = (unit.x, unit.y)
                                waypoints = self.find_path(entity_center, (slot_x, slot_y))
                                if waypoints:
                                    unit.waypoints = waypoints
                                    unit.target_position = (slot_x, slot_y)
                                if hasattr(unit, "stop_working"):
                                    unit.stop_working()
                    else:
                        # Comportamiento para 1 sola unidad seleccionada
                        unit = selected_units[0]
                        clicked_building = None
                        if getattr(unit, "entity_type") in ["Man", "Woman"]:
                            for building in self.buildings:
                                if building.get_collision_rect().collidepoint(world_x, world_y) and building.type in ["mill"]:
                                    clicked_building = building
                                    break
                        if getattr(unit, "entity_type") in ["Soldier", "Machine"]:
                            for building in self.buildings:
                                if building.get_collision_rect().collidepoint(world_x, world_y) and building.type in ["trench"]:
                                    clicked_building = building
                                    break

                        if clicked_building is None:             
                            if getattr(unit, "entity_type", None) in ["Soldier", "Machine"] and getattr(unit, "assigned_building", None) is not None:
                                if hasattr(unit, "un_trench"):
                                    unit.un_trench((world_x, world_y))
                            else:
                                entity_center = (unit.x, unit.y)
                                waypoints = self.find_path(entity_center, (world_x, world_y))
                                if waypoints:
                                    unit.waypoints = waypoints
                                    unit.target_position = (world_x, world_y)
                                if hasattr(unit, "stop_working"):
                                    unit.stop_working()    
                        elif clicked_building is not None:
                            slot = clicked_building.get_available_slot(unit)
                            if slot is not None:
                                unit.assigned_building = clicked_building
                                unit.assigned_slot = slot
                                clicked_building.highlight()
                                
                                if getattr(unit, "entity_type") in ["Man", "Woman"]: 
                                    target_x, target_y = slot["pos"]
                                    waypoints = self.find_path((unit.x, unit.y), (target_x + 32, target_y + 16))
                                    if waypoints:
                                        unit.waypoints = waypoints
                                        unit.target_position = (target_x, target_y)
                                elif getattr(unit, "entity_type") in ["Soldier", "Machine"]:
                                    door1_x, door1_y = clicked_building.get_left_door()
                                    door2_x, door2_y = clicked_building.get_right_door()
                                    d_to_left = self.get_distance(door1_x, door1_y, unit)
                                    d_to_right = self.get_distance(door2_x, door2_y, unit)
                                    if d_to_left <= d_to_right:
                                        target_x, target_y = door1_x, door1_y
                                    else:
                                        target_x, target_y = door2_x, door2_y    
                                    waypoints = self.find_path((unit.x, unit.y), (target_x, target_y))
                                    if waypoints:
                                        unit.waypoints = waypoints
                                        unit.target_position = (target_x, target_y)


    def render(self, surface: pygame.Surface) -> None:
        self.tilemap.render(surface, self.camera)
        for building in self.buildings:
            building.render(surface, self.camera)
        for entity in self.entitys:
            entity.render(surface, self.camera)

        # Renderizar rectángulo de selección por arrastre (drag box select)
        if self.is_dragging:
            x1, y1 = self.drag_start
            x2, y2 = self.drag_end
            world_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            screen_rect = self.camera.apply(world_rect)

            sel_surface = pygame.Surface((max(1, screen_rect.width), max(1, screen_rect.height)), pygame.SRCALPHA)
            sel_surface.fill((0, 255, 0, 40))  # Verde translúcido
            surface.blit(sel_surface, (screen_rect.x, screen_rect.y))
            pygame.draw.rect(surface, (0, 255, 0), screen_rect, 2)