from src.InTheTrenchOnTheFront import inTheTrenchOnTheFront

import pygame

pygame.mixer.set_num_channels(64)


if __name__ =="__main__":
    game = inTheTrenchOnTheFront()
    game.exec()

