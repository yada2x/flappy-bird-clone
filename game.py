import pygame
import sys
import random

from scripts.utils import load_image, load_images
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
            'bird-up': load_image("bird/yellow/yellowbird-upflap.png"),
            'numbers': load_images("nums"),
            'gameover': load_image("gameover.png")
        }

        self.sfx = {
            'death': pygame.mixer.Sound('assets/audio/die.wav'),
            'hit': pygame.mixer.Sound('assets/audio/hit.wav'),
            'point': pygame.mixer.Sound('assets/audio/point.wav'),
            'swoosh': pygame.mixer.Sound('assets/audio/swoosh.wav'),
            'wing': pygame.mixer.Sound('assets/audio/wing.wav')
        }

        self.sfx['death'].set_volume(0.5)
        self.sfx['hit'].set_volume(0.5)
        self.sfx['point'].set_volume(0.5)
        self.sfx['swoosh'].set_volume(0.5)
        self.sfx['wing'].set_volume(0.5)

    def reset(self):
        self.sfx['swoosh'].play()
        self.score = 0
        self.touching = False
        self.bird = Bird(self, "bird-mid", (70, 200), (34, 24))
        self.bg = random.choice(("day", "night"))
        self.pipe_spawner = PipeSpawner(self, "pipe", self.screen.get_width() + 104, (52, 320), 3, 100 )
        self.spawn_time = 0

    def gameover(self):
        while True:
            self.display.blit(self.assets[self.bg], (0, 0))
            self.bird.render(self.display)
            self.pipe_spawner.render(self.display)
            self.display.blit(self.assets["base"], (-self.base_pos, 400))
            self.display.blit(self.assets['gameover'], (self.display.get_width()//2 - self.assets['gameover'].get_width()//2, self.display.get_height()//3.5))
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            start = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        start = True
            if start:
                break

    def run(self):
        self.reset()
        self.base_pos = 0
        while True:
            # Update Screen
            self.display.fill((0, 0, 0, 0))
            self.display.blit(self.assets[self.bg], (0, 0))

            alive = self.bird.update()
            self.bird.render(self.display)
                
            collide = self.bird.collisions(self.pipe_spawner.get_rects(), self.pipe_spawner.get_point_rects()) if alive else 0
            if collide and not self.touching:
                self.touching = True
                self.sfx['point'].play()
                self.score += 1
            elif not collide:
                self.touching = False

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
                            self.sfx['wing'].play()
                            self.bird.jump()
            
            self.display.blit(self.assets["base"], (-self.base_pos, 400)) # So this is rendered over the bird and pipes
            self.base_pos = (self.base_pos + 3) % 48 if alive else 0
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

            # End state
            if not alive:
                self.pipe_spawner.speed = 0
                if self.bird.floored:
                    self.sfx['hit'].play()
                    self.sfx['death'].play()
                    self.gameover()
                    self.reset()

Game().run()