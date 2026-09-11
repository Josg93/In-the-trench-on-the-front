from typing import Any
from src import mixins
from gale.state import StateMachine
from src import states
import pygame

class GameEntity(mixins.AnimatedMixin, mixins.DrawableMixin):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        animations: dict,
        speed: float = 50.0,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.speed = speed
        self.animations = {}
        self.current_animation = None
        self.frame_index = 0
        self.flipped = False
        self.selected = False
        self.target_position = None
        self.generate_animations(animations)

        self.state_machine = StateMachine({
            "idle": states.entity_states.IdleState,
            "walk": states.entity_states.WalkState,
            "work": states.entity_states.WorkState,
        })
        self.state_machine.entity = self
        self.state_machine.change("idle")

    def update(self, dt: float) -> None:
        if self.target_position is not None:
            target_x, target_y = self.target_position
            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist < 5.0:
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

                current_state = self.state_machine.current
                if not isinstance(current_state, states.entity_states.WalkState) or getattr(current_state, "direction", None) != direction:
                    self.state_machine.change("walk", direction=direction)

        self.state_machine.update(dt)
        super().update(dt)

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        super().render(surface, camera)
        if self.selected:
            dest = camera.apply(pygame.Rect(self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, (0, 255, 0), dest, 2)

