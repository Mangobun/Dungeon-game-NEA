from settings import *
from support import scale_image, scale_pos

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('images', 'player', 'movement', 'down', '0.png')).convert_alpha()
        
        # fix scaling issue
        width = self.image.get_width() * SCALE
        height = self.image.get_height() * SCALE
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-90, -90)

        # movement
        self.direction = pygame.Vector2() # default values are 0,0 so left empty
        self.speed = 500
        self.collision_sprites = collision_sprites

        # combat
        self.attacking = False
        self.attack_cooldown = 400 # milliseconds
        self.attack_time = 0
        self.attack_hitbox = None

        # animation speed
        self.move_animation_speed = 5
        self.attack_animation_speed = 9

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        self.attack_frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, _, file_names in walk(join('images', 'player', 'movement', state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        surf = scale_image(surf)
                        self.frames[state].append(surf)

        for state in self.attack_frames.keys():
            for folder_path, _, file_names in walk(join('images', 'player', 'attack', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        surf = scale_image(surf)
                        self.attack_frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        # movement
        if not self.attacking:
            self.direction.x = (int(keys[pygame.K_d]) or int(keys[pygame.K_RIGHT])) - (int(keys[pygame.K_a]) or int(keys[pygame.K_LEFT]))
            self.direction.y = (int(keys[pygame.K_s]) or int(keys[pygame.K_DOWN])) - (int(keys[pygame.K_w]) or int(keys[pygame.K_UP]))
            self.direction = self.direction.normalize() if self.direction else self.direction
        else:
            self.direction = pygame.Vector2()

        # attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack_hitbox = self.get_attack_hitbox()
            self.frame_index = 0

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def attack_timer(self):
        if self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.attack_hitbox = None

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right =  sprite.rect.left # moving right
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right # moving left
                else:
                    if self.direction.y < 0: self.hitbox_rect.top =  sprite.rect.bottom # moving up 
                    if self.direction.y > 0: self.hitbox_rect.bottom =  sprite.rect.top # moving down 

    def get_attack_hitbox (self):
        hitbox_width, hitbox_height = 60, 60
        
        if self.state == 'right':
            return pygame.Rect(
                self.hitbox_rect.right,
                self.hitbox_rect.centery - hitbox_height // 2,
                hitbox_width,
                hitbox_height
            )
        if self.state == 'left':
            return pygame.Rect(
                self.hitbox_rect.left - hitbox_width,
                self.hitbox_rect.centery - hitbox_height // 2,
                hitbox_width,
                hitbox_height
            )

        if self.state == 'up':
            return pygame.Rect(
                self.hitbox_rect.centerx - hitbox_width // 2,
                self.hitbox_rect.top - hitbox_height,
                hitbox_width,
                hitbox_height
            )

        if self.state == 'down':
            return pygame.Rect(
                self.hitbox_rect.centerx - hitbox_width // 2,
                self.hitbox_rect.bottom,
                hitbox_width,
                hitbox_height
            )

    def animate(self, dt):
        old_center = self.rect.center
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'    

        # choose animation set
        if self.attacking:
            frames = self.attack_frames[self.state]
            self.frame_index += self.attack_animation_speed * dt
        else:
            frames = self.frames[self.state]
            self.frame_index = self.frame_index + self.move_animation_speed * dt if self.direction else 0

        # animate
        self.image = frames[int(self.frame_index) % len(frames)]
        self.rect = self.image.get_frect(center = old_center)

    def update(self, dt):
        self.input()
        self.move(dt)
        self.attack_timer()
        self.animate(dt)
