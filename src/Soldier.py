from typing import Any

from pygame import Surface
from src.GameEntity import GameEntity 

class Soldier(GameEntity):
    def __init__(self,
                 x: float,
                 y: float, 
                 width: float, 
                 height: float, 
                 texture_id: str, 
                 animations: dict, 
                 speed: float = 60, 
                 battlefield: Any = None, 
                 entity_type: str = "Man",
                 is_enemy: bool = False) -> None:
        super().__init__(x, y, width, height, texture_id, animations, speed, battlefield, entity_type)
        self.is_enemy = is_enemy
    def update(self, dt: float) -> None:
        return super().update(dt)
    
    def shoot(self):
        pass
    
    def trench(self):
        #meterse en trinchera
        pass
    
    def render(self, surface: Surface, camera: Any) -> None:
        return super().render(surface, camera)    