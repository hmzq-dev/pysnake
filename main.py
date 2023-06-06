import pygame
import random
import sys


pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 12
ENTITY_SIZE = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("PySnake")


snake = []
direction = "right"
score = 0

class SnakeBody(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((ENTITY_SIZE, ENTITY_SIZE))
        self.surf.fill("green")

        if len(snake) == 0:
            self.rect = self.surf.get_rect(
                center=(SCREEN_WIDTH/3, SCREEN_HEIGHT/2)
            )
        else:
            self.rect = self.surf.get_rect(
                right=snake[-1].rect.x,
                top=snake[-1].rect.y
            )


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((ENTITY_SIZE, ENTITY_SIZE))
        self.surf.fill("red")

        if score == 0:
            self.rect = self.surf.get_rect(
                center=(SCREEN_WIDTH*(3/4), SCREEN_HEIGHT/2)
            )
        else:
            randx = random.randint(0, SCREEN_WIDTH-ENTITY_SIZE)
            randy = random.randint(0, SCREEN_HEIGHT-ENTITY_SIZE)
            self.rect = self.surf.get_rect(
                x=randx,
                y=randy
            )


def grow_snake(n=1):
    for i in range(0, n):
        snake.append(SnakeBody())

grow_snake(6)
apple = Apple()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "down":
                direction = "up"
            elif event.key == pygame.K_DOWN and direction != "up":
                direction = "down"
            elif event.key == pygame.K_RIGHT and direction != "left":
                direction = "right"
            elif event.key == pygame.K_LEFT and direction != "right":
                direction = "left"

    # Move snake
    for snake_body in snake:
        if snake_body is snake[0]:
            tmp = (snake_body.rect.x, snake_body.rect.y)
            new_pos = (snake_body.rect.x, snake_body.rect.y)
            if direction == "up":
                snake_body.rect.move_ip(0, -ENTITY_SIZE)
            elif direction == "down":
                snake_body.rect.move_ip(0, ENTITY_SIZE)
            elif direction == "right":
                snake_body.rect.move_ip(ENTITY_SIZE, 0)
            elif direction == "left":
                snake_body.rect.move_ip(-ENTITY_SIZE, 0)
        else:
            tmp = (snake_body.rect.x, snake_body.rect.y)
            snake_body.rect.x, snake_body.rect.y = new_pos
            new_pos = tmp

    # Check if apple is eaten
    if pygame.sprite.collide_rect(snake[0], apple):
        score += 1
        grow_snake()
        print(score)
        apple = Apple()
        # Checking if new apple collides with the snake
        for snake_body in snake:
            if pygame.sprite.collide_rect(snake_body, apple):
                apple = Apple()

    screen.fill("black")
    for snake_body in snake:
        screen.blit(snake_body.surf, snake_body.rect)

    screen.blit(apple.surf, apple.rect)

    pygame.display.flip()

    clock.tick(FPS)
