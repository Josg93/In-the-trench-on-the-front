from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import Text, render_text 

import pygame
import settings

class StartState(BaseState):
    def enter(self):
        #pygame.mixer.music.play(loops=-1)
        pass
    def render(self, surface : pygame.Surface):
        surface.blit(settings.TEXTURES["background"],(0 , 0) )
        #self.title.render(surface)
        
        render_text(
            surface,
            "In The trench on the front",
            settings.FONTS["big"],
            settings.VIRTUAL_WIDTH // 2,
            170,
            (197, 195, 198),
            center= True,
            shadowed=True,
        )
        
        render_text(
            surface,
            "Press Enter",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + 40,
            (197, 195, 198),
            center=True,
            shadowed=True,
        )
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("play", 1)
