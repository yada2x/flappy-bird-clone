import pygame
import sys
import os

BASE_IMG_PATH = "assets/sprites/"

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img = pygame.Surface.convert_alpha(img)
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img))
    return images