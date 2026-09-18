from typing import Any
from src import mixins
import pygame

class GameBuilding(mixins.DrawableMixin, mixins.CollidableMixin):
    """
    Representa una estructura en el campo de batalla (edificio civil o militar).
    Soporta hitboxes de colisión personalizados (parciales) mediante offsets y dimensiones.
    """
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
        work_slots = [],
    ) -> None:
        self.type = type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.frame_index = frame_index
        self.hp = hp
        self.max_hp = max_hp 
        self.flipped = False
        self.collidable = collidable
        self.active = True
        self.solid = solid
        self.collision_offset_x = collision_offset_x
        self.collision_offset_y = collision_offset_y
        self.collision_width = collision_width if collision_width is not None else width
        self.collision_height = collision_height if collision_height is not None else height
        self.highlight_timer = 0
        self.is_enemy = is_enemy
        self.work_slots = work_slots
        # Inicializar puestos de trabajo (slots) alrededor del edificio (especialmente para el molino)
        
        if self.type == "mill":
            self.work_slots = [
                {"pos": (self.x + 24, self.y + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 64 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 96 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 128 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 160 + 40), "occupied": False, "assigned_entity": None},
                
                {"pos": (self.x + 290, self.y + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 290, self.y + 64 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 290, self.y + 96 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 290, self.y + 128 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 290, self.y + 160 + 40), "occupied": False, "assigned_entity": None},
            ]
            
        if self.type == "trench":
            self.work_slots = [
                {"pos": (self.x + 24, self.y + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 64 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 96 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 128 + 40), "occupied": False, "assigned_entity": None},
                {"pos": (self.x + 24, self.y + 160 + 40), "occupied": False, "assigned_entity": None},
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

    def highlight(self):
        self.highlight_timer = 1.0

    def update(self, dt: float) -> None:
        if self.highlight_timer > 0:
            self.highlight_timer -= dt

    def get_collision_rect(self) -> pygame.Rect:
        """
        Retorna el rectángulo de colisión ajustado con los offsets de colisión parcial.
        """
        return pygame.Rect(
            round(self.x + self.collision_offset_x),  
            round(self.y + self.collision_offset_y),
            self.collision_width,
            self.collision_height,
        )

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        super().render(surface, camera)
        if self.highlight_timer > 0:
            rect = self.get_collision_rect()
            applied_rect = camera.apply(rect)
            pygame.draw.rect(surface, (255, 255, 0), applied_rect, 3)

        if hasattr(self, "hp") and hasattr(self, "max_hp") and self.hp < self.max_hp:
            bar_width = self.width
            bar_height = 6
            bar_x = self.x
            bar_y = self.y - 10
            dest = camera.apply(pygame.Rect(bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(surface, (200, 0, 0), dest)
            current_width = max(0, int(bar_width * (self.hp / self.max_hp)))
            current_rect = pygame.Rect(dest.x, dest.y, current_width, bar_height)
            pygame.draw.rect(surface, (0, 200, 0), current_rect)
            pygame.draw.rect(surface, (255, 255, 255), dest, 1)