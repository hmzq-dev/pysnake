import pygame
import neat
import os
import pickle
import sys
from .game_config import *
from . import Game


class GameAI(Game):
    def __init__(self):
        super().__init__()


    def train(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.started = True
        genome_high_score = 0
        timer = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.event_handler(event)

            # AI makes a decision
            output = net.activate((
                self.snake[0].rect.x - self.apple.rect.x,
                self.snake[0].rect.y - self.apple.rect.y,
                self.can_move("up"),
                self.can_move("down"),
                self.can_move("right"),
                self.can_move("left"),
            ))
            decision = output.index(max(output))
            if decision == 0:
                self.direction = "up"
            elif decision == 1:
                self.direction = "down"
            elif decision == 2:
                self.direction = "right"
            elif decision == 3:
                self.direction = "left"

            if self.started and not self.snake_is_dead:
                self.move_snake()
                self.detect_collisions()

            if self.score > genome_high_score:
                genome_high_score = self.score
                timer = 0

            # End training for genome
            if self.snake_is_dead:
                genome.fitness += self.score
                self.reset()
                break
            
            # To avoid infinite loops
            if self.score == genome_high_score and timer == FPS*30:
                genome.fitness -= 3
                self.reset()
                break

            timer += 1
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)


    def can_move(self, direction):
        # 0 -> Shouldnt move (snake body or wall)
        # 1 -> Can move
        # 2 -> Should move (apple)
        if direction == "up":
            for snake_body in self.snake[1:]:
                if snake_body.rect.x == self.snake[0].rect.x and snake_body.rect.y == self.snake[0].rect.y - ENTITY_SIZE:
                    return 0 
                
            if self.snake[0].rect.y - ENTITY_SIZE < 0 or direction == "down":
                return 0
            else:
                if self.apple.rect.x == self.snake[0].rect.x and self.apple.rect.y == self.snake[0].rect.y - ENTITY_SIZE:
                    return 2
                return 1
            
        if direction == "down":
            for snake_body in self.snake[1:]:
                if snake_body.rect.x == self.snake[0].rect.x and snake_body.rect.y == self.snake[0].rect.y + ENTITY_SIZE:
                    return 0 
                
            if self.snake[0].rect.y + ENTITY_SIZE == SCREEN_HEIGHT or direction == "up":
                return 0
            else:
                if self.apple.rect.x == self.snake[0].rect.x and self.apple.rect.y == self.snake[0].rect.y + ENTITY_SIZE:
                    return 2
                return 1
            
        if direction == "right":
            for snake_body in self.snake[1:]:
                if snake_body.rect.x == self.snake[0].rect.x + ENTITY_SIZE and snake_body.rect.y == self.snake[0].rect.y:
                    return 0 
                
            if self.snake[0].rect.x + ENTITY_SIZE == SCREEN_WIDTH or direction == "left":
                return 0
            else:
                if self.apple.rect.x == self.snake[0].rect.x + ENTITY_SIZE and self.apple.rect.y == self.snake[0].rect.y:
                    return 2
                return 1
            
        if direction == "left":
            for snake_body in self.snake[1:]:
                if snake_body.rect.x == self.snake[0].rect.x - ENTITY_SIZE and snake_body.rect.y == self.snake[0].rect.y:
                    return 0 
                
            if self.snake[0].rect.x - ENTITY_SIZE < 0 or direction == "right":
                return 0
            else:
                if self.apple.rect.x == self.snake[0].rect.x - ENTITY_SIZE and self.apple.rect.y == self.snake[0].rect.y:
                    return 2
                return 1


    def test(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.started = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.event_handler(event)

            # AI makes a decision
            output = net.activate((
                self.snake[0].rect.x - self.apple.rect.x,
                self.snake[0].rect.y - self.apple.rect.y,
                self.can_move("up"),
                self.can_move("down"),
                self.can_move("right"),
                self.can_move("left"),
            ))
            decision = output.index(max(output))
            if decision == 0:
                self.direction = "up"
            elif decision == 1:
                self.direction = "down"
            elif decision == 2:
                self.direction = "right"
            elif decision == 3:
                self.direction = "left"

            if self.started and not self.snake_is_dead:
                self.move_snake()
                self.detect_collisions()


            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)


    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = 0
            self.train(genome, config)


    def run_neat(self, config):
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())
        p.add_reporter(neat.Checkpointer(
            generation_interval=5, 
            time_interval_seconds=2500,
            filename_prefix="neat-checkpoints/neat-checkpoint-"
        ))

        winner = p.run(self.eval_genomes, 100)
        with open("neat-models/best.pickle", "wb") as f:
            pickle.dump(winner, f)


def load_config():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    return config
