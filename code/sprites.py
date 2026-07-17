from settings import *
from random import randint

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
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites, enemy_type, heart_frames, heart_groups):
        super().__init__(groups)
        self.player = player

        # image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 5

        # heart
        self.heart_frames = heart_frames
        self.heart_groups = heart_groups  

        # rect
        self.rect = self.image.get_frect(center = pos)

        if enemy_type == 'bat':
            self.hitbox_rect = self.rect.inflate(-40, -50)
        if enemy_type == 'blob':
            self.hitbox_rect = self.rect.inflate(5, -40)

        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()

        # attributes
        self.enemy_type = enemy_type
        if enemy_type == 'bat':
            self.speed = 350
        elif enemy_type == 'blob':
            self.speed = 150

        if enemy_type == 'bat':
            self.notice_radius = 250
        elif enemy_type == 'blob':
            self.notice_radius = 400

        # timer
        self.death_time = 0
        self.death_duration = 400

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def move(self, dt):
        # get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()
        distance = player_pos.distance_to(enemy_pos)

        if distance < self.notice_radius:
            self.direction = (player_pos - enemy_pos).normalize()
        else:
            self.direction = pygame.Vector2()

        # update the rect position + collision
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collisions('vertical')
        self.rect.center = self.hitbox_rect.center

    def collisions(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left 
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right 
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom  
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top 

    def destroy(self):
        # start a timer
        self.death_time = pygame.time.get_ticks()

        # change the image
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:

            # heart drop
            if self.player.health < self.player.max_health:
                if randint(1, 100) <= 30:
                    HeartPickup(self.rect.center, self.heart_frames, self.heart_groups)

            self.kill()

    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
            
class HeartPickup(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        # animation
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 4

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

        # timer
        self.spawn_time = pygame.time.get_ticks()
        self.life_duration = 10000
        self.flash_duration = 3000

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.life_duration - self.flash_duration:
            if current_time // 100 % 2 == 0:
                self.image.set_alpha(80)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        if elapsed_time >= self.life_duration:
            self.kill()

    def update(self, dt):
        self.animate(dt)
        self.timer()

