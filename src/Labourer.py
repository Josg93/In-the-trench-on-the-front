from typing import Any

from pygame import Surface
from src.GameEntity import GameEntity 

class Labourer(GameEntity):
    def __init__(self,
                 x: float,
                 y: float, 
                 width: float, 
                 height: float, 
                 texture_id: str, 
                 animations: dict, 
                 speed: float = 60, 
                 battlefield: Any = None, 
                 entity_type: str = "Man") -> None:
        super().__init__(x, y, width, height, texture_id, animations, speed, battlefield, entity_type)
        
    def update(self, dt: float) -> None:
        return super().update(dt)
    
    def work(self):
        self.state_machine.change("work")
    
    def render(self, surface: Surface, camera: Any) -> None:
        return super().render(surface, camera)    