
from typing import Any
from gale.state import BaseState
from src.GameBattlefield import GameBattlefield
from src.Labourer import Labourer
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
            
    def update(self, dt: float) -> None:
        self.battlefield.update(dt)
        
        self.scroll(dt)

        # manejar actividades de las entidades y producción de comida
        working_count = 0
        for entity in self.battlefield.entitys:
            if entity.assigned_building is not None:   
                if getattr(entity, "entity_type", "Man") in ["Man", "Woman"]:
                    entity_rect =  entity.get_collision_rect()
                    if entity_rect.colliderect(entity.assigned_building.get_collision_rect()):
                        entity.work()  
                        
                if getattr(entity, "entity_type", "") == "Soldier":
                    entity_rect =  entity.get_collision_rect()
                    if entity_rect.colliderect(entity.assigned_building.get_collision_rect()):
                        if hasattr(entity, "trench"):
                            entity.trench() 

            if hasattr(entity, "state_machine") and entity.state_machine and hasattr(entity.state_machine, "current"):
                from src.states.entity_states.WorkState import WorkState
                if isinstance(entity.state_machine.current, WorkState):
                    working_count += 1

        if working_count > 0:
            self.battlefield.food += 1.0 * dt * working_count
                
                
    def on_input(self, input_id: str, input_data: Any) -> None:
        if hasattr(self.battlefield, "on_input"):
            self.battlefield.on_input(input_id, input_data)

    def render(self, surface: pygame.Surface) -> None:
        self.battlefield.render(surface)
        box_rect = pygame.Rect(self.camera.x -670, self.camera.y -350, 220, 60)
        applied_rect = self.camera.apply(box_rect)
        pygame.draw.rect(surface, (50, 50, 50), applied_rect)
        pygame.draw.rect(surface, (255, 255, 255), applied_rect, 2)
        
        food_text = settings.FONTS["medium"].render(f"Food: {int(self.battlefield.food)}", True, (255, 255, 255))
        entities_text = settings.FONTS["medium"].render(f"Entities: {len(self.battlefield.entitys)}", True, (255, 255, 255))
        
        surface.blit(food_text, (applied_rect.x + 10, applied_rect.y + 8))
        surface.blit(entities_text, (applied_rect.x + 10, applied_rect.y + 32))
