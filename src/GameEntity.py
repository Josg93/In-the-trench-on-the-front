from typing import Any
from src import mixins
from gale.state import StateMachine
import pygame

class GameEntity(mixins.AnimatedMixin, mixins.DrawableMixin):
    """
    Entidad del juego (labourer, soldier) que gestiona su movimiento,
    máquina de estados, selección y colisiones con edificios sólidos.
    """
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        animations: dict,
        speed: float = 60.0,
        battlefield: Any = None,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.speed = speed
        self.battlefield = battlefield
        self.animations = {}
        self.current_animation = None
        self.frame_index = 0
        self.flipped = False
        self.selected = False
        self.target_position = None
        self.waypoints = []
        self.generate_animations(animations)

        from src import states
        self.state_machine = StateMachine({
            "idle": states.entity_states.IdleState,
            "walk": states.entity_states.WalkState,
            "work": states.entity_states.WorkState,
        })
        self.state_machine.entity = self
        self.state_machine.change("idle")

    def get_collision_rect(self) -> pygame.Rect:
        # Rectángulo de colisión de la entidad (enfocado en la parte inferior para perspectiva 2.5D)
        return pygame.Rect(round(self.x), round(self.y + self.height * 0.5), self.width, self.height * 0.5)

    def update(self, dt: float) -> None:
        if self.waypoints:
            target_x, target_y = self.waypoints[0]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist < 5.0:
                self.waypoints.pop(0)
                if not self.waypoints:
                    self.x = target_x
                    self.y = target_y
                    self.target_position = None
                    self.state_machine.change("idle")
            else:
                if abs(dx) > abs(dy):
                    direction = "right" if dx > 0 else "left"
                else:
                    direction = "down" if dy > 0 else "up"

                move_x = (dx / dist) * self.speed * dt
                move_y = (dy / dist) * self.speed * dt

                self.x += move_x
                self.y += move_y

                from src import states
                current_state = self.state_machine.current
                if self.waypoints and (not isinstance(current_state, states.entity_states.WalkState) or getattr(current_state, "direction", None) != direction):
                    self.state_machine.change("walk", direction=direction)

        self.state_machine.update(dt)
        super().update(dt)

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        super().render(surface, camera)
        if self.selected:
            dest = camera.apply(pygame.Rect(self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, (0, 255, 0), dest, 2)
