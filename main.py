import pygame
import random
import sys


pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 10
ENTITY_SIZE = 20
SNAKE_LENGTH_INITIAL = 6
FONT_SIZE = 16
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("PySnake")
font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)


class SnakeBody(pygame.sprite.Sprite):
    def __init__(self):
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
    def __init__(self):
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


def grow_snake(n=1):
    for i in range(0, n):
        snake.append(SnakeBody())

snake = []
grow_snake(SNAKE_LENGTH_INITIAL)
direction = "right"
score = 0
high_score = 0
started = False
dead = False
apple = Apple()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if started:
                if dead:
                    # Reset game
                    snake = []
                    grow_snake(SNAKE_LENGTH_INITIAL)
                    direction = "right"
                    score = 0
                    dead = False
                    apple = Apple()

                else:
                    if event.key == pygame.K_UP and direction != "down":
                        direction = "up"
                    elif event.key == pygame.K_DOWN and direction != "up":
                        direction = "down"
                    elif event.key == pygame.K_RIGHT and direction != "left":
                        direction = "right"
                    elif event.key == pygame.K_LEFT and direction != "right":
                        direction = "left"
            else:
                started = True

    if started and not dead:
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
            if score > high_score:
                high_score = score
            grow_snake()
            apple = Apple()
            # Checking if new apple collides with the snake
            for snake_body in snake:
                if pygame.sprite.collide_rect(snake_body, apple):
                    apple = Apple()

        # Check if snake head collides with body
        for snake_body in snake:
            if not snake_body is snake[0]:
                if pygame.sprite.collide_rect(snake_body, snake[0]):
                    dead = True
        # Or with vertical walls
        if snake[0].rect.x < 0 or snake[0].rect.x == SCREEN_WIDTH:
            dead = True
        # Or with horizontal walls
        if snake[0].rect.y < 0 or snake[0].rect.y == SCREEN_HEIGHT:
            dead = True


    screen.fill("black")
    for snake_body in snake:
        screen.blit(snake_body.surf, snake_body.rect)

    screen.blit(apple.surf, apple.rect)

    # Update text boxes
    if started:
        text = font.render(f"Score: {score}, High Score: {high_score}", True, "white")
    else:
        text = font.render("Press any key to start. Use the arrow keys to move.", True, "white")

    screen.blit(text, (ENTITY_SIZE, ENTITY_SIZE))

    if dead:
        text = font.render("Game Over! Press any key to play again.", True, "white")
        screen.blit(text, (ENTITY_SIZE, ENTITY_SIZE+FONT_SIZE*2))
    
    pygame.display.flip()

    clock.tick(FPS)
