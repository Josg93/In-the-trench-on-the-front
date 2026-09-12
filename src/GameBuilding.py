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
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        frame_index: int,
        collidable: bool = True,
        solid: bool = False,
        collision_offset_x: float = 0,
        collision_offset_y: float = 0,
        collision_width: float = None,
        collision_height: float = None,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.frame_index = frame_index
        self.flipped = False
        self.collidable = collidable
        self.active = True
        self.solid = solid
        self.collision_offset_x = collision_offset_x
        self.collision_offset_y = collision_offset_y
        self.collision_width = collision_width if collision_width is not None else width
        self.collision_height = collision_height if collision_height is not None else height

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
