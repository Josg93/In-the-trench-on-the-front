import pygame


#importar archivos de Gale 
from gale.game import Game
from gale.state import StateMachine
from gale.input_handler import InputData 

from src.states import game_states

import settings


class inTheTrenchOnTheFront(Game):
    
    def init(self)->None:
        
        self.state_machine = StateMachine(
            {
                "start" : game_states.StartState,
                "menu" : game_states.MenuState,
                "play" : game_states.PlayState,
                "defeat" : game_states.DefeatState,
                "victory" : game_states.VictoryState,
                "tutorial": game_states.TutorialState,
                "mision1" : game_states.MisionState, 
            }
        )
        
        self.state_machine.change("start")
               
    def update(self , dt :float)->None:
        self.state_machine.update(dt)
        
        
    def render(self , surface : pygame.surface)->None:
        self.state_machine.render(surface)
            
    def on_input(self, input_id: str, input_data: InputData)->None:
        if input_id == "quit" and input_data == "Pressed":
            self.quit()
        else:
            self.state_machine.on_input(input_id, input_data)
                       