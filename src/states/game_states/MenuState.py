from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import Text, render_text 
from gale.timer import Timer

import pygame
import settings

class MenuState(BaseState):
    def enter(self):
        
        self.transition_alpha = 255
        self.transitioning = False
        
        Timer.tween(1, [(self, {"transition_alpha": 0})])
        
    def render(self, surface : pygame.Surface):
        imagen_escalada = pygame.transform.scale(settings.TEXTURES["menu"] ,
                                                 (settings.WINDOW_WIDTH ,
                                                  settings.WINDOW_HEIGHT ))
        surface.blit(imagen_escalada,(0 , 10) )
        
        
        
        
        
        if self.transition_alpha > 0:
            fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.transition_alpha))
            surface.blit(fade_surface, (0, 0))
            
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if self.transition_alpha <= 0: 
            if input_id == "enter" and input_data.pressed:
                self.state_machine.change("mision1")

        