
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


        # manejar actividades de las entidades
        for entity in self.battlefield.entitys:
            if entity.assigned_building is not None:   
                 
                if entity.type in ["Man", "Woman"]:
                    entity_rect =  entity.get_collision_rect()
                    if entity_rect.colliderect(entity.assigned_building.get_collision_rect()):
                        entity.work()  
                        
                if entity.type == ["Soldier"]:
                    entity_rect =  entity.get_collision_rect()
                    if entity_rect.colliderect(entity.assigned_building.get_collision_rect()):
                        entity.trench() 
                
                
    def on_input(self, input_id: str, input_data: Any) -> None:
        if hasattr(self.battlefield, "on_input"):
            self.battlefield.on_input(input_id, input_data)

    def render(self, surface: pygame.Surface) -> None:
        square_rect = pygame.Rect(self.camera.x, self.camera.y, 20, 20)
        pygame.draw.rect(surface, (255, 0, 0), self.camera.apply(square_rect))
        self.battlefield.render(surface)
