import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
FPS = 16
SPEED = 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("PySnake")


snake = []
direction = "right"

class SnakeBody(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((25, 25))
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

def grow_snake(n):
    for i in range(0, n):
        snake.append(SnakeBody())

grow_snake(6)


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
                snake_body.rect.move_ip(0, -SPEED)
            elif direction == "down":
                snake_body.rect.move_ip(0, SPEED)
            elif direction == "right":
                snake_body.rect.move_ip(SPEED, 0)
            elif direction == "left":
                snake_body.rect.move_ip(-SPEED, 0)
        else:
            tmp = (snake_body.rect.x, snake_body.rect.y)
            snake_body.rect.x, snake_body.rect.y = new_pos
            new_pos = tmp

    screen.fill("black")

    for snake_body in snake:
        screen.blit(snake_body.surf, snake_body.rect)

    pygame.display.flip()


    clock.tick(FPS)