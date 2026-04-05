from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'movement', 'down', '0.png')).convert_alpha()
        
        # fix scaling issue
        scale = 5
        width = self.image.get_width() * scale
        height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect

        # movement
        self.direction = pygame.Vector2() # default values are 0,0 so left empty
        self.speed = 500
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_d]) or int(keys[pygame.K_RIGHT])) - (int(keys[pygame.K_a]) or int(keys[pygame.K_LEFT]))
        self.direction.y = (int(keys[pygame.K_s]) or int(keys[pygame.K_DOWN])) - (int(keys[pygame.K_w]) or int(keys[pygame.K_UP]))
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right =  sprite.rect.left # moving right
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right # moving left
                else:
                    if self.direction.y < 0: self.hitbox_rect.top =  sprite.rect.bottom # moving up 
                    if self.direction.y > 0: self.hitbox_rect.bottom =  sprite.rect.top # moving down 

    def update(self, dt):
        self.input()
        self.move(dt)