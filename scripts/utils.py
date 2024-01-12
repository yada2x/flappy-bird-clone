import pygame
import sys

BASE_IMG_PATH = "assets/sprites/"

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img = pygame.Surface.convert_alpha(img)
    img.set_colorkey((0, 0, 0))
    return img

def gameover():
        while True:
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