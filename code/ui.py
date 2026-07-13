from settings import *
from support import scale_image, scale_pos

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.load_images()

        
    def load_images(self):
        self.full_heart = pygame.image.load(join('images', 'hearts', 'health', 'full_heart.png')).convert_alpha()
        self.half_heart = pygame.image.load(join('images', 'hearts', 'health', 'half_heart.png')).convert_alpha()
        self.empty_heart = pygame.image.load(join('images', 'hearts', 'health', 'empty_heart.png')).convert_alpha()

        self.full_heart = scale_image(self.full_heart, SCALE * 1.3)
        self.half_heart = scale_image(self.half_heart, SCALE * 1.3)
        self.empty_heart = scale_image(self.empty_heart, SCALE * 1.3)

    def display(self, health):
        for i in range(3):
            x = 25 + i * 90
            y = 25

            heart_value = health - (i * 2)

            if heart_value >= 2:
                image = self.full_heart
            elif heart_value == 1:
                image = self.half_heart
            else:
                image = self.empty_heart

            self.display_surface.blit(image, (x, y))
