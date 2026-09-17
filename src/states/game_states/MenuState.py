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
        imagen_escalada = pygame.transform.scale(settings.TEXTURES["white1"] ,
                                                 (settings.WINDOW_WIDTH // 2,
                                                  settings.WINDOW_HEIGHT ))
        surface.blit(imagen_escalada,(0 , 0) )
        imagen_escalada2 = pygame.transform.scale(settings.TEXTURES["white3"] ,
                                                 (settings.WINDOW_WIDTH // 2 + 300,
                                                  settings.WINDOW_HEIGHT ))
        surface.blit(imagen_escalada2,(settings.WINDOW_WIDTH //  2 , 0) )
        #self.title.render(surface)
        
        render_text(
            surface,
            "Liderais al ejercito blanco",
            settings.FONTS["big"],
            settings.VIRTUAL_WIDTH - settings.VIRTUAL_WIDTH // 4,
            170,
            (197, 195, 198),
            center= True,
            shadowed=True,
        )
        
        render_text(
            surface,
            "Tu deber es evitar que los bolcheviques", 
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH - settings.VIRTUAL_WIDTH // 4,
            190,
            (197, 195, 198),
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "se hagan con el poder", 
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH - settings.VIRTUAL_WIDTH // 4,
            200,
            (197, 195, 198),
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Repele el ataque enemigo ",
            settings.FONTS["big"],
            settings.VIRTUAL_WIDTH - settings.VIRTUAL_WIDTH // 4,
            settings.VIRTUAL_HEIGHT // 2 + 100,
            (197, 195, 198),
            center= True,
            shadowed=True,
        )
        render_text(
            surface,
            "para lograr la victoria",
            settings.FONTS["big"],
            settings.VIRTUAL_WIDTH - settings.VIRTUAL_WIDTH // 4,
            settings.VIRTUAL_HEIGHT // 2 + 130,
            (197, 195, 198),
            center= True,
            shadowed=True,
        )
        
        
        
        if self.transition_alpha > 0:
            fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.transition_alpha))
            surface.blit(fade_surface, (0, 0))
            
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if self.transition_alpha <= 0: 
            if input_id == "enter" and input_data.pressed:
                self.state_machine.change("play", 1)

        