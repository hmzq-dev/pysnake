import pysnake
from pysnake.game_config import *
import pygame
import sys

game = pysnake.Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        game.event_handler(event)

    if game.started and not game.snake_is_dead:
        game.move_snake()
        game.detect_collisions()

    game.draw()
    pygame.display.flip()
    game.clock.tick(FPS)
