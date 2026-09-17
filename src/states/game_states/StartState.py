from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import Text, render_text 
from gale.timer import Timer

import pygame
import settings

class StartState(BaseState):
    def enter(self):
        pygame.mixer.music.load(settings.BASE_DIR / "assets" / "sounds" / "menu_theme.mp3"),
        
        pygame.mixer.music.play(loops=-1)
        self.transition_alpha = 255
        self.show = 0
        self.transitioning = False
        
        Timer.tween(4, [(self, {"transition_alpha": 0})])
        Timer.tween(8, [(self, {"show": 1})])
        
    def render(self, surface : pygame.Surface):
        surface.blit(settings.TEXTURES["background"],(0 , 0) )
        
        if self.show == 1:
            #self.title.render(surface)
            ancho_panel = settings.WINDOW_WIDTH // 4
            alto_panel = 400

            # 3. Crear la superficie transparente DEL TAMAÑO DEL PANEL
            alpha_surface = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)

            # 4. Dibujar el rectángulo relativo a alpha_surface (empieza en 0, 0)
            # Relleno con opacidad
            pygame.draw.rect(alpha_surface, (40, 40, 40, 128), (0, 0, ancho_panel, alto_panel))
            # Borde blanco (completamente opaco)
            pygame.draw.rect(alpha_surface, (255, 255, 255, 255), (0, 0, ancho_panel, alto_panel), 2)

            # 5. Pegar el panel en la pantalla en la posición real
            pos_x = settings.WINDOW_WIDTH // 3 + 90
            pos_y = 300
            
            surface.blit(alpha_surface, (pos_x, pos_y))
            
            render_text(
            surface,
            "Press Enter",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + 40,
            (197, 195, 198),
            center=True,
            shadowed=True,) 

        
        render_text(
            surface,
            "In The trench on the front",
            settings.FONTS["title"],
            settings.VIRTUAL_WIDTH // 2,
            170,
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
                self.state_machine.change("menu")

        