from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        # Ground first
        for sprite in self:
            if getattr(sprite, 'type', None) == 'ground':
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Details second
        for sprite in self:
            if getattr(sprite, 'type', None) == 'detail':
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Everything else sorted
        for sprite in sorted(self, key = lambda sprite: sprite.rect.centery):
            if getattr(sprite, 'type', None) not in ('ground', 'detail'):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
