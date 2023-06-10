import pygame
from .game_config import *
import random


class SnakeBody(pygame.sprite.Sprite):
    def __init__(self, snake):
        super().__init__()
        self.surf = pygame.Surface((ENTITY_SIZE, ENTITY_SIZE))

        if len(snake) == 0:
            self.surf.fill("green3")
            self.rect = self.surf.get_rect(
                x=SCREEN_WIDTH/3, 
                y=SCREEN_HEIGHT/2
            )
        else:
            self.surf.fill("green4")
            self.rect = self.surf.get_rect(
                right=snake[-1].rect.x,
                top=snake[-1].rect.y
            )



class Apple(pygame.sprite.Sprite):
    def __init__(self, score):
        super().__init__()
        self.surf = pygame.Surface((ENTITY_SIZE, ENTITY_SIZE))
        self.surf.fill("red")

        if score == 0:
            self.rect = self.surf.get_rect(
                x=SCREEN_WIDTH*(2/3),
                y=SCREEN_HEIGHT/2
            )
        else:
            randx = random.randint(0, SCREEN_WIDTH-ENTITY_SIZE)
            randy = random.randint(0, SCREEN_HEIGHT-ENTITY_SIZE)
            while randx % ENTITY_SIZE != 0 or randy % ENTITY_SIZE != 0:
                randx = random.randint(0, SCREEN_WIDTH-ENTITY_SIZE)
                randy = random.randint(0, SCREEN_HEIGHT-ENTITY_SIZE)
            self.rect = self.surf.get_rect(
                x=randx,
                y=randy
            )
