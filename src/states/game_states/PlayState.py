
from typing import Any
from gale.state import BaseState
from src.GameBattlefield import GameBattlefield
import pygame

class PlayState(BaseState):
    def enter(self, level: Any = 1) -> None:
        self.battlefield = GameBattlefield(level)

    def update(self, dt: float) -> None:
        self.battlefield.update(dt)

    def on_input(self, input_id: str, input_data: Any) -> None:
        if hasattr(self.battlefield, "on_input"):
            self.battlefield.on_input(input_id, input_data)

    def render(self, surface: pygame.Surface) -> None:
        self.battlefield.render(surface)
