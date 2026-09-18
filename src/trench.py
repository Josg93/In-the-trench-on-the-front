from typing import Any
from src.GameBuilding import GameBuilding
import pygame 

class Trench(GameBuilding):
    def __init__(
        self,
        type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        frame_index: int,
        hp: int ,
        max_hp : int,
        collidable: bool = True,
        solid: bool = False,
        collision_offset_x: float = 0,
        collision_offset_y: float = 0,
        collision_width: float = None,
        collision_height: float = None,
        is_enemy: bool = False,
        ) -> None:
        
        super().__init__(
            type, x, y, width, height, texture_id, frame_index, hp, max_hp,
            collidable, solid, collision_offset_x, collision_offset_y,
            collision_width, collision_height, is_enemy, work_slots=[]
        )
        
        self.work_slots = [
                {"pos": (self.x + 166, self.y + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 64 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 96 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 128 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 160 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 192 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 224 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 256 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 288 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 320 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 352 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 384 + 107), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 166, self.y + 416 + 107), "occupied": False, "assigned_entity": None},
            ]
        
    def get_available_slot(self, entity: Any) -> dict:
        self.free_slot(entity)
        for slot in self.work_slots:
            if slot["occupied"] is False:
                slot["occupied"] = True
                slot["assigned_entity"] = entity
                return slot
        return None

    

    def free_slot(self, entity: Any):
        """
        Libera el slot que estaba ocupado por la entidad especificada.
        """
        for slot in self.work_slots:
            if slot["assigned_entity"] == entity:
                slot["occupied"] = False
                slot["assigned_entity"] = None
                
                
    def get_left_door(self):
        left_door = pygame.Rect(round(self.x + 80) , round(self.y + 164),80,86) 
        return (left_door.x + 40 , left_door.y + 43)
        
    def get_right_door(self):
        right_door = pygame.Rect(round(self.x + 341) , round(self.y + 150),80,86)
        return (right_door.x + 40, right_door.y + 43) 
