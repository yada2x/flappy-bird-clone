import pygame
import sys

from scripts.utils import load_image

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
            'bird-down': load_image("bird/yellow/yellowbird-downflap.png"),
            'bird-mid': load_image("bird/yellow/yellowbird-midflap.png"),
            'bird-up': load_image("bird/yellow/yellowbird-upflap.png")
        }

        self.jump = False

    def run(self):
        while True:
            # Update Screen
            self.display.fill((0, 0, 0, 0))
            self.display.blit(self.assets['day'], (0, -12))

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
                    if event.key == pygame.K_SPACE:
                        self.jump = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.jump = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()