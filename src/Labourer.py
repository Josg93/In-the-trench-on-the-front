from typing import Any

from pygame import Surface
from src.GameEntity import GameEntity 
from gale.timer import Timer

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
        self.is_working = False
        
    def update(self, dt: float) -> None:
        return super().update(dt)
    
    def work(self):
        if not self.is_working:
            self.is_working = True
            self.work_timer = Timer.every(1, lambda: setattr(self.battlefield, 'food', self.battlefield.food + 10))
            self.state_machine.change("work")

    def stop_working(self):
        if self.is_working:
            self.is_working = False
            if hasattr(self, "work_timer") and self.work_timer:
                self.work_timer.remove()
                self.work_timer = None
            self.assigned_building = None
            self.state_machine.change("idle")
    
    def render(self, surface: Surface, camera: Any) -> None:
        return super().render(surface, camera)    