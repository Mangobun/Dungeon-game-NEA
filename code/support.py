from settings import *
import pygame

def scale_image(image, scale = SCALE):
    return pygame.transform.scale(
        image,
        (image.get_width() * scale, image.get_height() * scale)
    )

def scale_pos(x, y):
    return x * SCALE, y * SCALE
