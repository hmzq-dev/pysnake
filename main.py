from pysnake import Game
from pysnake.ai import GameAI, load_neat_config
from pysnake.game_config import *
import pygame
import pyautogui
import pickle
import os

pygame.init()
pygame.font.init()

display_width, display_height = pyautogui.size()

# Ask for a choice
choices = ["a", "x"]
decision = ""
while not decision in choices:
    os.system("cls")
    print(f"""
Which mode would you like to choose?
[a] Play myself
[x] Run the AI

        """)
    decision = input("> ")

# Let player play the game
if decision == "a":
    game = Game()
    # Focus mouse on game screen
    pyautogui.moveTo(display_width/2, display_height/2)
    pyautogui.click()

    while True:
        res = game.handle_events()
        if res == "back":
            break

        if game.started and not game.snake_is_dead:
            game.move_snake()
            game.detect_collisions()

        game.draw()
        pygame.display.flip()
        game.clock.tick(FPS)

# Run AI
elif decision == "x":
    neat_config = load_neat_config()
    game = GameAI()
    # Focus mouse on game screen
    pyautogui.moveTo(display_width/2, display_height/2)
    pyautogui.click()

    with open("neat-models/best.pickle", "rb") as f:
        winner = pickle.load(f)

    while True:
        game.test(winner, neat_config)
