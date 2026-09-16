from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import Text, render_text 
from gale.timer import Timer
import pygame

import settings

class DefeatState(BaseState):
    def enter(self):
        pygame.mixer.music.load(settings.BASE_DIR / "assets" / "sounds" / "red_victory.mp3"),
        pygame.mixer.music.play(loops=-1)
        self.transition_alpha = 255
        self.transitioning = False
        
        Timer.tween(4, [(self, {"transition_alpha": 0})])
        
        
    def render(self, surface : pygame.Surface):
        surface.blit(settings.TEXTURES["red_victory"],(0 , 0) )
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
            "You has been defeated",
            settings.FONTS["big"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 ,
            (197, 195, 198),
            center=True,
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
        
          
        if self.transition_alpha > 0:
            fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.transition_alpha))
            surface.blit(fade_surface, (0, 0))
        
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("start")
