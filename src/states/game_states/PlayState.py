
from typing import Any
from gale.state import BaseState
from src.GameBattlefield import GameBattlefield
import pygame

class PlayState(BaseState):
    def enter(self, level: Any = 1) -> None:
        self.battlefield = GameBattlefield(level)

    def update(self, dt: float) -> None:
        self.battlefield.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.battlefield.render(surface)