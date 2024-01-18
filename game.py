import pygame
import sys
import random

from scripts.utils import load_image, gameover
from scripts.entities import PhysicsObject, Pipe, PipeSpawner, Bird

class Game():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Flappy Bird Clone")

        self.screen = pygame.display.set_mode((576, 1000))
        self.display = pygame.Surface((288, 512), pygame.SRCALPHA)     
        self.clock = pygame.time.Clock()
        
        self.assets = {
            'day': load_image("background/background-day.png"),
            'night': load_image("background/background-night.png"),
            'base': load_image("base.png"),
            'pipe': load_image("pipe/pipe-green.png"),
            'bird-down': load_image("bird/yellow/yellowbird-downflap.png"),
            'bird-mid': load_image("bird/yellow/yellowbird-midflap.png"),
            'bird-up': load_image("bird/yellow/yellowbird-upflap.png")
        }

    def reset(self):
        self.bird = Bird(self, "bird-mid", (70, 200), (34, 24))
        self.bg = random.choice(("day", "night"))
        self.pipe_spawner = PipeSpawner(self, "pipe", self.screen.get_width() + 104, (52, 320), 3, 100 )
        self.spawn_time = 0

    def run(self):
        self.reset()
        base_pos = 0
        while True:
            # Update Screen
            self.display.fill((0, 0, 0, 0))
            self.display.blit(self.assets[self.bg], (0, 0))

            alive = self.bird.update()
            self.bird.render(self.display)
            self.bird.collisions(self.pipe_spawner.get_rects())

            self.spawn_time += 1
            if self.spawn_time >= 60 and alive:
                self.pipe_spawner.add_pipe()
                self.spawn_time = 0
            self.pipe_spawner.update(self.pipe_spawner.speed)
            self.pipe_spawner.render(self.display)

            # Input Manager
            event: pygame.Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key == pygame.K_SPACE:
                        if alive:
                            self.bird.jump()
            
            self.display.blit(self.assets["base"], (-base_pos, 400)) # So this is rendered over the bird and pipes
            base_pos = (base_pos + 3) % 48 if alive else 0
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

            # End state
            if not alive:
                self.pipe_spawner.speed = 0 
                if self.bird.floored:
                    gameover()
                    self.reset()

Game().run()