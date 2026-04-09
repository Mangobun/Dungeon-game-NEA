from settings import *
import pygame

def scale_image(image):
    return pygame.transform.scale(
        image,
        (image.get_width() * SCALE, image.get_height() * SCALE)
    )

def scale_pos(x, y):
    return x * SCALE, y * SCALE
