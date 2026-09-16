from typing import Any
from gale.state import BaseState
from src.GameBattlefield import GameBattlefield
from src.Labourer import Labourer
from src.Soldier import Soldier
from src.definitions import Entitys
from src.mixins import DrawableMixin
from gale.camera import Camera
from gale.timer import Timer, Tween
import random
import pygame
import settings

class PlayState(BaseState , DrawableMixin):
    def enter(self, level: Any = 1) -> None:
        self.fade_alpha = 255
        Tween(3, [(self, {"fade_alpha": 0})])
        self.camera = Camera(
            settings.VIRTUAL_WIDTH,
            settings.VIRTUAL_HEIGHT,
            x=0,
            y=1280,
            bounds=pygame.Rect(0, 0,16000 , 1280)
        )
        self.battlefield = GameBattlefield(level, self.camera)
        
        # Wave system initialization
        self.wave = 1
        self.enemies_remaining = 10  # 10 * 2^(wave-1) for wave 1
        self.wave_intervals = [0, 30, 30, 30, 30]#[30, 60, 120, 240, 480]  # seconds, doubles each wave (index 0 = before wave 1)
        self.time_until_next_wave = self.wave_intervals[0]  # 30 seconds for first wave
       
        self.game_won = False
        
        self.transition_alpha = 255
        self.transitioning = False
        
        #temporizador de fade in fade out
        Timer.tween(4, [(self, {"transition_alpha": 0})])
    
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
        target_y = random.randint(655,1171)
        if self.battlefield.food >= 100 and type == "labourer":
            target_pos = (417, target_y)
            self.battlefield.food -= 100
            gender = random.randint(0,1)
            if gender == 0:
                definition = Entitys.LABOURERS["Man"].copy()
            elif gender == 1:    
                definition = Entitys.LABOURERS["Woman"].copy()
            
            spawn_x = 300
            spawn_y = 863
            birth_way = self.battlefield.find_path((spawn_x, spawn_y), target_pos)
            
            new_labourer = Labourer(
                x=spawn_x,
                y=spawn_y,
                width=64,
                height=96,
                battlefield=self.battlefield,
                entity_type="Man",
                waypoints=birth_way,
                target_position=target_pos,
                **definition
            )
            self.battlefield.entitys.append(new_labourer)
            
        elif self.battlefield.food >= 200 and type == "soldier":
            # Comprobar que exista al menos 1 barracks aliado
            has_barracks = any(
                building.type == "barracks" and not getattr(building, "is_enemy", False)
                for building in self.battlefield.buildings
            )
            if not has_barracks:
                return

            self.battlefield.food -= 200
            target_y = random.randint(655,1000)
            target_pos = (3532,target_y)
            definition = Entitys.SOLDIERS["Soldier"].copy()
            
            spawn_x, spawn_y = 400, 863  # Valor por defecto si se encuentra un barracks se sobreescribe
            for building in self.battlefield.buildings:
                if building.type == "barracks" and not getattr(building, "is_enemy", False):
                    spawn_x, spawn_y = (building.x + building.get_collision_rect().width // 2 ,
                                        (building.y + building.get_collision_rect().height) + 120)
                    break
            
            
            birth_way = self.battlefield.find_path((spawn_x, spawn_y), target_pos)
            
            new_soldier = Soldier(
                x=spawn_x,
                y=spawn_y,
                width=64,
                height=96,
                battlefield=self.battlefield,
                entity_type="Soldier",
                waypoints=birth_way,
                target_position=target_pos,
                **definition
            )
            self.battlefield.entitys.append(new_soldier)
    
    def spawn_enemy_wave(self , wave : int) -> None:
        """
        Genera una oleada de soldados enemigos desde el extremo derecho del mapa
        con el objetivo de avanzar hacia el borde izquierdo (x = 0).
        """
        if wave > 5:
            # Wave 5 completed, player wins
            self.state_machine.change("victory")
            return
            
        definition = Entitys.SOLDIERS["Soldier_enemy"].copy()
        
        # Enemies per wave: 10, 20, 40, 80, 160 (doubling)
        enemies_this_wave = 10 * (2 ** (wave - 1))
        self.enemies_remaining = enemies_this_wave
        
        for i in range(enemies_this_wave):
            y = random.randint(655,1100)
            spawn_x = 7750 # 15500
            spawn_y = y
            left_edge = (320, spawn_y)

            birth_way = self.battlefield.find_path((spawn_x, spawn_y), left_edge)
            enemy_soldier = Soldier(
                x=spawn_x,
                y=spawn_y,
                width=64,
                height=96,
                battlefield=self.battlefield,
                entity_type="Soldier_enemy",
                waypoints=birth_way,
                target_position=left_edge,
                **definition
            )
            self.battlefield.entitys.append(enemy_soldier)
    
    def update(self, dt: float) -> None:
        self.battlefield.update(dt)
        self.scroll(dt)

        # Update wave timer
        self.time_until_next_wave -= dt

        if self.time_until_next_wave <= 0:
            # Spawn current wave
            self.spawn_enemy_wave(self.wave)
            # Set next interval (doubles each wave)
            if self.wave < 5:
                self.time_until_next_wave = self.wave_intervals[self.wave]  # wave 1->index 1 (60s), etc.
        
        if self.battlefield.capitol.hp <= 0:
            self.state_machine.change("defeat")
        
        # Check if all enemies current wave are defeated
        alive_enemies = [e for e in self.battlefield.entitys if getattr(e, "hp", 0) > 0 and getattr(e, "is_enemy", False)]
        
        if not alive_enemies and self.enemies_remaining == 0 and not self.game_won:
            # Current wave enemies all defeated
            self.wave += 1
            if self.wave > 5:
                # All waves completed, player wins
                self.game_won = True
                self.state_machine.change("victory")
            # else: next wave will spawn when timer triggers
        
        # Check win condition after wave 5 with no enemies
        if self.wave > 5 and not self.game_won and len(alive_enemies) == 0:
            self.game_won = True
            self.state_machine.change("victory")
    
    def on_input(self, input_id: str, input_data: Any) -> None:
        if input_id == "enter" and input_data.pressed:
            print("in the trench!")
        elif input_id == "select_entity" and hasattr(input_data, "pressed") and input_data.pressed:
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


        # ----------------- Panel de oleada: tiempo restante y numero de oleada ----------
        waves_rect = pygame.Rect(self.camera.x + 500, self.camera.y - 350, 220, 60)
        applied_waves_rect = self.camera.apply(waves_rect)
        pygame.draw.rect(surface, (50, 50, 50), applied_waves_rect)
        pygame.draw.rect(surface, (255, 255, 255), applied_waves_rect, 2)
        
        # Time remaining for next wave
        time_remaining = max(0, int(self.time_until_next_wave))
        time_text = settings.FONTS["medium"].render(f"Time: {time_remaining}s", True, (255, 255, 255))
        wave_text = settings.FONTS["medium"].render(f"Wave: {self.wave}", True, (255, 255, 255))
        
        surface.blit(time_text, (applied_waves_rect.x + 10, applied_waves_rect.y + 8))
        surface.blit(wave_text, (applied_waves_rect.x + 10, applied_waves_rect.y + 32))
        
        if self.transition_alpha > 0:
            fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.transition_alpha))
            surface.blit(fade_surface, (0, 0))