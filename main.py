import pygame
import pickle

pygame.init()
pygame.font.init()

from pysnake.ai import GameAI, load_config


config = load_config()
game = GameAI()

# Trainig AI
# game.run_neat(config)

# Testing AI
with open("neat-models/best.pickle", "rb") as f:
    winner = pickle.load(f)
game.test(winner, config)


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#         game.event_handler(event)

#     if game.started and not game.snake_is_dead:
#         game.move_snake()
#         game.detect_collisions()

#     game.draw()
#     pygame.display.flip()
#     game.clock.tick(FPS)
