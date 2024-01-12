import pygame

BASE_IMG_PATH = "flappy-bird-assets/sprites/"

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img = pygame.Surface.convert_alpha(img)
    img.set_colorkey((0, 0, 0))
    return img