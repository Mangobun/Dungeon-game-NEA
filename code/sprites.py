from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, sprite_type = None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.type = sprite_type

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        