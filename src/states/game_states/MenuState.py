import pygame
import settings
from gale.state import BaseState

class MenuState(BaseState):
    def enter(self):
        pygame.mixer.music.play(loops=-1)
        
    def render(self):
        pass