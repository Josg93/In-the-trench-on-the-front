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
        self.selected_index = 0
        
        Timer.tween(1, [(self, {"transition_alpha": 0})])
        
    def render(self, surface : pygame.Surface):
        imagen_escalada = pygame.transform.scale(settings.TEXTURES["menu"] ,
                                                 (settings.WINDOW_WIDTH ,
                                                  settings.WINDOW_HEIGHT ))
        surface.blit(imagen_escalada,(0 , 10) )
        
        siguiente_color = (255, 255, 0) if self.selected_index == 0 else (197, 195, 198)
        tutorial_color = (255, 255, 0) if self.selected_index == 1 else (197, 195, 198)

        render_text(
            surface,
            ("> " + "Siguiente" + " <") if self.selected_index == 0 else "Siguiente",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2 + 180,
            settings.VIRTUAL_HEIGHT - 80,
            siguiente_color,
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            ("> " + "Tutorial" + " <") if self.selected_index == 1 else "Tutorial",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2 + 300,
            settings.VIRTUAL_HEIGHT - 80,
            tutorial_color,
            center=True,
            shadowed=True,
        )
        
        if self.transition_alpha > 0:
            fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.transition_alpha))
            surface.blit(fade_surface, (0, 0))
            
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if self.transition_alpha <= 0: 
            if input_id in ("left", "right") and input_data.pressed:
                self.selected_index = 1 - self.selected_index
            elif input_id == "enter" and input_data.pressed:
                if self.selected_index == 0:
                    self.state_machine.change("mision1")
                else:
                    self.state_machine.change("tutorial")

        