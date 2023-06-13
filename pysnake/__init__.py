import pygame
from .game_config import *
from .sprites import SnakeBody, Apple
import sys



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
        pygame.display.set_caption("PySnake")

        self.high_score = 0
        self.started = False
        self.reset()


    def reset(self):
        self.snake = [SnakeBody([])]
        self.direction = "right"
        self.score = 0
        self.snake_is_dead = False
        self.apple = Apple(self.score)

        for i in range(0, SNAKE_LENGTH_INITIAL-1):
            self.snake.append(SnakeBody(self.snake))


    def move_snake(self):
        for snake_body in self.snake:
            if snake_body is self.snake[0]:
                tmp = (snake_body.rect.x, snake_body.rect.y)
                new_pos = (snake_body.rect.x, snake_body.rect.y)
                if self.direction == "up":
                    snake_body.rect.move_ip(0, -ENTITY_SIZE)
                elif self.direction == "down":
                    snake_body.rect.move_ip(0, ENTITY_SIZE)
                elif self.direction == "right":
                    snake_body.rect.move_ip(ENTITY_SIZE, 0)
                elif self.direction == "left":
                    snake_body.rect.move_ip(-ENTITY_SIZE, 0)
            else:
                tmp = (snake_body.rect.x, snake_body.rect.y)
                snake_body.rect.x, snake_body.rect.y = new_pos
                new_pos = tmp


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.started:
                    if self.snake_is_dead and event.key == pygame.K_a:
                        self.reset()
                    else:
                        if event.key == pygame.K_UP and self.direction != "down":
                            self.direction = "up"
                        elif event.key == pygame.K_DOWN and self.direction != "up":
                            self.direction = "down"
                        elif event.key == pygame.K_RIGHT and self.direction != "left":
                            self.direction = "right"
                        elif event.key == pygame.K_LEFT and self.direction != "right":
                            self.direction = "left"
                else:
                    self.started = True


    def detect_collisions(self):
        # Check is apple is eaten
        if pygame.sprite.collide_rect(self.snake[0], self.apple):
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.snake.append(SnakeBody(self.snake))
            self.apple = Apple(self.score)

            # Checking if new apple collides with the snake
            for snake_body in self.snake:
                if pygame.sprite.collide_rect(snake_body, self.apple):
                    self.apple = Apple(self.score)

        # Check is snake head touches its body
        for snake_body in self.snake:
            if not snake_body is self.snake[0]:
                if pygame.sprite.collide_rect(snake_body, self.snake[0]):
                    self.snake_is_dead = True
        # Or with vertical walls
        if self.snake[0].rect.x < 0 or self.snake[0].rect.x == SCREEN_WIDTH:
            self.snake_is_dead = True
        # Or with horizontal walls
        if self.snake[0].rect.y < 0 or self.snake[0].rect.y == SCREEN_HEIGHT:
            self.snake_is_dead = True


    def draw(self):
        self.screen.fill("black")
        for snake_body in self.snake:
            self.screen.blit(snake_body.surf, snake_body.rect)
        self.screen.blit(self.apple.surf, self.apple.rect)

        # Update text boxes
        if self.started:
            text = self.font.render(f"Score: {self.score}, High Score: {self.high_score}", True, "white")
        else:
            text = self.font.render("Press any key to start. Use the arrow keys to move.", True, "white")

        self.screen.blit(text, (ENTITY_SIZE, ENTITY_SIZE))

        if self.snake_is_dead:
            text = self.font.render("Game Over! Press 'A' to play again.", True, "white")
            self.screen.blit(text, (ENTITY_SIZE, ENTITY_SIZE+FONT_SIZE*2))
