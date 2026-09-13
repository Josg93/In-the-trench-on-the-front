
from typing import Any
from gale.state import BaseState
from src.GameBattlefield import GameBattlefield
from src.Labourer import Labourer
from src.Soldier import Soldier
from src.definitions import Entitys
from src.mixins import DrawableMixin
from gale.camera import Camera

import pygame
import settings

class PlayState(BaseState , DrawableMixin):
    def enter(self, level: Any = 1) -> None:
        self.camera = Camera(
            settings.VIRTUAL_WIDTH,
            settings.VIRTUAL_HEIGHT,
            x=0,
            y=1280,
            bounds=pygame.Rect(0, 0,16000 , 1280)
        )
        self.battlefield = GameBattlefield(level, self.camera)
        # Temporizadores para las oleadas de enemigos tras 30 segundos
        self.game_timer = 0.0
        self.enemy_spawn_timer = 0.0
        self.enemies_started = False
    
    def mouse_to_virtual(self, mouse_x : float , mouse_y : float ):
        virtual_mouse_x = mouse_x * (settings.VIRTUAL_WIDTH / settings.WINDOW_WIDTH)
        virtual_mouse_y = mouse_y * (settings.VIRTUAL_HEIGHT / settings.WINDOW_HEIGHT)
        return (virtual_mouse_x, virtual_mouse_y)
            
    def scroll(self , dt : float):
        # manejo de la camara:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        virtual_mouse_x , virtual_mouse_y = self.mouse_to_virtual(mouse_x, mouse_y)

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
    
    def generate_entity(self, type : str) -> None:
        
        if self.battlefield.food >= 100 and type == "labourer":
            target_pos = (417, 862)
            self.battlefield.food -= 100
            definition = Entitys.LABOURERS["Man"].copy()
            
            spawn_x = 10
            spawn_y = 863
            birth_way = self.battlefield.find_path((spawn_x, spawn_y), target_pos)
            
            new_labourer = Labourer(
                x=spawn_x,
                y=spawn_y,
                width=64,
                height=96,
                battlefield=self.battlefield,
                entity_type="Man",
                waypoints=[target_pos],
                target_position=target_pos,
                **definition
            )
            self.battlefield.entitys.append(new_labourer)
            
        elif self.battlefield.food >= 200 and type == "soldier":
            self.battlefield.food -= 200
            target_pos = (3532,811)
            definition = Entitys.SOLDIERS["Soldier"].copy()
            
            spawn_x = 200
            spawn_y = 1200
            for building in self.battlefield.buildings:
                if building.type == "barracks":
                    spawn_x, spawn_y = (building.x + building.width // 2, building.y + building.height)
            
            birth_way = self.battlefield.find_path((spawn_x, spawn_y), target_pos)
            
            new_soldier = Soldier(
                x=spawn_x,
                y=spawn_y,
                width=64,
                height=96,
                battlefield=self.battlefield,
                entity_type="Soldier",
                waypoints=[target_pos],
                target_position=target_pos,
                **definition
            )
            self.battlefield.entitys.append(new_soldier)

    def spawn_enemy_wave(self) -> None:
        """
        Genera una oleada de soldados enemigos desde el extremo derecho del mapa
        con el objetivo de avanzar hacia el borde izquierdo (x = 0).
        """
        definition = Entitys.SOLDIERS["Soldier_enemy"].copy()
        spawn_x = 15500
        spawn_y = 800
        left_edge = (0, spawn_y)

        for i in range(3):  # Spawnea 3 enemigos por oleada
            offset_y = spawn_y + (i * 50 - 50)
            birth_way = self.battlefield.find_path((spawn_x, offset_y), left_edge)
            enemy_soldier = Soldier(
                x=spawn_x,
                y=offset_y,
                width=64,
                height=96,
                battlefield=self.battlefield,
                entity_type="Soldier_enemy",
                waypoints=birth_way if birth_way else [left_edge],
                target_position=left_edge,
                **definition
            )
            self.battlefield.entitys.append(enemy_soldier)
    
    def update(self, dt: float) -> None:
        self.battlefield.update(dt)
        self.scroll(dt)

        # ----------------- Temporizador y Oleadas de Enemigos (30 segundos) -----------------
        self.game_timer += dt
        if self.game_timer >= 30.0:
            self.enemies_started = True
            self.enemy_spawn_timer += dt
            if self.enemy_spawn_timer >= 6.0:  # Cada 6 segundos genera una oleada de enemigos
                self.enemy_spawn_timer = 0.0
                self.spawn_enemy_wave()

        # ----------------- Gestión de objetivos de los enemigos ----------------------------
        # Los enemigos priorizan atacar a entidades amigas en rango; si no hay, avanzan hacia el borde izquierdo.
        for entity in self.battlefield.entitys:
            if getattr(entity, "is_enemy", False):
                attack_range = getattr(entity, "attack_range", 150.0)
                target_found = False

                for other in self.battlefield.entitys:
                    if not getattr(other, "is_enemy", False):
                        dist = ((other.x - entity.x) ** 2 + (other.y - entity.y) ** 2) ** 0.5
                        if dist <= attack_range:
                            target_found = True
                            # Detenerse para combatir
                            entity.waypoints = []
                            break

                # Si no hay amigos en rango y no tiene ruta activa, avanzar hacia la izquierda (x = 0)
                if not target_found and not entity.waypoints:
                    left_edge = (0, entity.y)
                    waypoints = self.battlefield.find_path((entity.x, entity.y), left_edge)
                    if waypoints:
                        entity.waypoints = waypoints
                        entity.target_position = left_edge
                    else:
                        entity.waypoints = [left_edge]
                        entity.target_position = left_edge

        # ----------------- manejar actividades de las entidades --------------------------
        for entity in self.battlefield.entitys:
            # poner a hacer algo a las entidades
            if entity.assigned_building is not None:
                #poner a trabajar a los labourers    
                if getattr(entity, "entity_type") in ["Man", "Woman"]:
                    entity_rect =  entity.get_work_rect()
                    if entity_rect.colliderect(entity.assigned_building.get_collision_rect()):
                        entity.work()  
                        
                # poner a trabajar a los soldiers        
                if getattr(entity, "entity_type", "") == "Soldier":
                    entity_rect =  entity.get_work_rect()
                    if entity_rect.colliderect(entity.assigned_building.get_collision_rect()):
                        if hasattr(entity, "trench"):
                            entity.trench() 
    
    
    def on_input(self, input_id: str, input_data: Any) -> None:
        if input_id == "select_entity" and hasattr(input_data, "pressed") and input_data.pressed:
            mouse_x, mouse_y = input_data.position
            virtual_mouse_x, virtual_mouse_y = self.mouse_to_virtual(mouse_x, mouse_y)
            world_x, world_y = self.camera.screen_to_world((virtual_mouse_x, virtual_mouse_y))

            panel_rect = pygame.Rect(self.camera.x - 670, self.camera.y + 230, settings.WINDOW_WIDTH, 116)
            labourer_btn_rect = pygame.Rect(panel_rect.x + 10, panel_rect.y + 10, 145, 96)
            soldier_btn_rect = pygame.Rect(panel_rect.x + 170, panel_rect.y + 10, 145, 96)

            if labourer_btn_rect.collidepoint(world_x, world_y):
                self.generate_entity("labourer")

            elif soldier_btn_rect.collidepoint(world_x, world_y):
                self.generate_entity("soldier")

        if hasattr(self.battlefield, "on_input"):
            self.battlefield.on_input(input_id, input_data)



    
               

    def render(self, surface: pygame.Surface) -> None:
        self.battlefield.render(surface)
        #-670 y -350
        #----------------------------- Panel de Recursos -----------------------------
        box_rect = pygame.Rect(self.camera.x -670, self.camera.y - 350, 220, 60)
        applied_rect = self.camera.apply(box_rect)
        pygame.draw.rect(surface, (50, 50, 50), applied_rect)
        pygame.draw.rect(surface, (255, 255, 255), applied_rect, 2)
        
        food_text = settings.FONTS["medium"].render(f"Food: {int(self.battlefield.food)}", True, (255, 255, 255))
        entities_text = settings.FONTS["medium"].render(f"Population: {len(self.battlefield.entitys)}", True, (255, 255, 255))
        
        surface.blit(food_text, (applied_rect.x + 10, applied_rect.y + 8))
        surface.blit(entities_text, (applied_rect.x + 10, applied_rect.y + 32))



        #----------------------------- Panel de Creacion de Unidades-----------------------------
        panel_rect = pygame.Rect(self.camera.x - 670, self.camera.y + 230, settings.WINDOW_WIDTH, 116)
        applied_panel_rect = self.camera.apply(panel_rect)
        pygame.draw.rect(surface, (40, 40, 40), applied_panel_rect)
        pygame.draw.rect(surface, (255, 255, 255), applied_panel_rect, 2)


        labourer_btn_rect = pygame.Rect(panel_rect.x +10, panel_rect.y + 10, 145, 96)
        soldier_btn_rect = pygame.Rect(panel_rect.x + 170, panel_rect.y + 10 , 145, 96)
        
        applied_labourer_btn_rect = self.camera.apply(labourer_btn_rect)
        applied_soldier_btn_rect = self.camera.apply(soldier_btn_rect)
         
        pygame.draw.rect(surface, (70, 70, 70), applied_labourer_btn_rect)
        pygame.draw.rect(surface, (200, 200, 200), applied_labourer_btn_rect, 1)
        pygame.draw.rect(surface, (70, 70, 70), applied_soldier_btn_rect)
        pygame.draw.rect(surface, (200, 200, 200), applied_soldier_btn_rect, 1)

        labourer_text = settings.FONTS["small"].render("Labourer (100)", True, (255, 255, 255))
        soldier_text = settings.FONTS["small"].render("Soldier (200)", True, (255, 255, 255))

        surface.blit(labourer_text, ( applied_labourer_btn_rect.x + 66,  applied_labourer_btn_rect.y + 38))
        surface.blit(soldier_text, (applied_soldier_btn_rect.x + 66, applied_soldier_btn_rect.y + 38))

        # Unit icons
        texture = settings.TEXTURES["entitys"]
        
        frame_lab = settings.FRAMES["entitys"][0]
        icon_lab = pygame.Surface((frame_lab.width, frame_lab.height), pygame.SRCALPHA)
        icon_lab.blit(texture, (0, 0), frame_lab)
        icon_lab_scaled = pygame.transform.scale(icon_lab, (64, 96))
        surface.blit(icon_lab_scaled, (applied_labourer_btn_rect.x , applied_labourer_btn_rect.y ))

        frame_sol = settings.FRAMES["entitys"][44]
        icon_sol = pygame.Surface((frame_sol.width, frame_sol.height), pygame.SRCALPHA)
        icon_sol.blit(texture, (0, 0), frame_sol)
        icon_sol_scaled = pygame.transform.scale(icon_sol, (64, 96))
        surface.blit(icon_sol_scaled, (applied_soldier_btn_rect.x , applied_soldier_btn_rect.y ))
