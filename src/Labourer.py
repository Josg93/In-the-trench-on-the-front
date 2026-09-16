from typing import Any

from pygame import Surface
from src.GameEntity import GameEntity 
from gale.timer import Timer

import settings 

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
                 entity_type: str = "Man",
                 waypoints : list = [],
                 target_position: tuple = None  
                 ) -> None:
                 
        super().__init__(x, y, width,height, texture_id, animations, speed, battlefield, entity_type, waypoints, target_position)
        self.is_working = False
        
    def update(self, dt: float) -> None:
        return super().update(dt)
    
    
    
    def work(self):
        self.harvesting()

    def stop_working(self):
        self.stop_harvesting()




# -------------------- COSECHAR TRIGO ---------------------
    def harvesting(self):
        if not self.is_working:
            self.is_working = True
            self.work_timer = Timer.every(1, lambda: setattr(self.battlefield, 'food', self.battlefield.food + 10))
            #self.harvesting_sound = Timer.every(10, lambda: settings.SOUNDS["harvesting"].play())
           
            self.state_machine.change("work")
    
    def stop_harvesting(self):
         if self.is_working:
            self.is_working = False
            if hasattr(self, "work_timer") and self.work_timer:
                #self.harvesting_sound
                self.work_timer.remove()
                self.work_timer = None
            if self.assigned_building and hasattr(self.assigned_building, "free_slot"):
                self.assigned_building.free_slot(self)
            self.assigned_building = None
            self.assigned_slot = None
            self.state_machine.change("idle")

# -------------------------------------------------        
    
    def render(self, surface: Surface, camera: Any) -> None:
        return super().render(surface, camera)    