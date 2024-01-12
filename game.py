import pygame
import sys
import random

from scripts.utils import load_image, gameover
from scripts.entities import PhysicsObject, Pipe, Bird

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
            'pipe': load_image("pipe/pipe-green.png"),
            'bird-down': load_image("bird/yellow/yellowbird-downflap.png"),
            'bird-mid': load_image("bird/yellow/yellowbird-midflap.png"),
            'bird-up': load_image("bird/yellow/yellowbird-upflap.png")
        }

    def reset(self):
        self.bird = Bird(self, "bird-mid", (70, 200), (34, 24))
        self.bk = random.choice(("day", "night"))

    def run(self):
        self.reset()
        while True:
            # Update Screen
            self.display.fill((0, 0, 0, 0))
            self.display.blit(self.assets[self.bk], (0, 0))

            alive = self.bird.update()
            self.bird.render(self.display)
            # print(self.bird.pos)

            if not alive and self.bird.pos[1] >= self.display.get_height() + self.bird.size[1]:
                gameover() # revamp this to enable white flash
                self.reset()

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
                        self.bird.jump()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()