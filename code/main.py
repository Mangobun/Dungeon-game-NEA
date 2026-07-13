from settings import *
from player import Player
from sprites import *
from groups import AllSprites
from support import scale_image, scale_pos
from ui import UI

from pytmx.util_pygame import load_pygame
from random import randint, choice

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Dungeon Game')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.pickup_sprites = pygame.sprite.Group()

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 1500)
        self.spawn_positions = []
        
        # ui
        self.ui = UI()

        # setup
        self.load_images()
        self.setup()

    def load_images(self):
        # enemies
        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images','enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    surf = scale_image(surf)
                    self.enemy_frames[folder].append(surf)

        # hearts
        self.heart_frames = []
        for folder_path, _, file_names in walk(join('images', 'hearts', 'animation')):
            for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                full_path = join(folder_path, file_name)
                surf = pygame.image.load(full_path).convert_alpha()
                surf = scale_image(surf)
                self.heart_frames.append(surf)
        

    def setup(self):
        map = load_pygame(join('data', 'maps', 'dungeon.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            image = scale_image(image)
            Sprite((x * SCALED_TILE_SIZE, y * SCALED_TILE_SIZE), image, self.all_sprites, sprite_type = 'ground')

        for x, y, image in map.get_layer_by_name('Details').tiles():
            image = scale_image(image)
            Sprite((x * SCALED_TILE_SIZE, y * SCALED_TILE_SIZE), image, self.all_sprites, sprite_type = 'detail')

        for obj in map.get_layer_by_name('Objects'):
            image = scale_image(obj.image)
            x, y = scale_pos(obj.x, obj.y)

            CollisionSprite((x, y), image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            x, y = scale_pos(obj.x, obj.y)
            width = obj.width * SCALE
            height = obj.height * SCALE

            surf = pygame.Surface((width, height))
            CollisionSprite((x, y), surf, self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                x, y = scale_pos(obj.x, obj.y)
                self.player = Player((x, y), self.all_sprites, self.collision_sprites)
            else:
                x, y = scale_pos(obj.x, obj.y)
                self.spawn_positions.append((x, y))

    def attack_collision(self):
        if self.player.attack_hitbox:
            for enemy in self.enemy_sprites:
                if enemy.death_time == 0 and enemy.hitbox_rect.colliderect(self.player.attack_hitbox):
                    enemy.destroy()

    def player_collision(self):
        if not self.player.attacking and not self.player.invincible:
            for enemy in self.enemy_sprites:
                if enemy.death_time == 0 and enemy.hitbox_rect.colliderect(self.player.damage_rect):
                    self.player.health = max(self.player.health - 1, 0)
                    self.player.invincible = True
                    self.player.damage_time = pygame.time.get_ticks()
                    break

    def pickup_collision(self):
        for pickup in self.pickup_sprites:
            if pickup.rect.colliderect(self.player.damage_rect):
                self.player.health = min(self.player.health + 2, self.player.max_health)
                pickup.kill()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    spawn_pos = choice(self.spawn_positions)
                    can_spawn = True

                    for enemy in self.enemy_sprites:
                        distance = pygame.Vector2(enemy.rect.center).distance_to(spawn_pos)

                        if distance < 350:
                            can_spawn = False

                    if can_spawn:
                        enemy_type = choice(list(self.enemy_frames.keys()))
                        Enemy(
                            spawn_pos, 
                            self.enemy_frames[enemy_type], 
                            (self.all_sprites, self.enemy_sprites), 
                            self.player, 
                            self.collision_sprites, 
                            enemy_type,
                            self.heart_frames,
                            (self.all_sprites, self.pickup_sprites)
                            )

            # update
            self.all_sprites.update(dt)
            self.attack_collision()
            self.player_collision()
            self.pickup_collision()

            # draw
            self.display_surface.fill(COLORS['background'])
            self.all_sprites.draw(self.player.rect.center)
            self.ui.display(self.player.health)

            # temporary hitbox visibility
            # if self.player.attack_hitbox:
            #     offset_hitbox = self.player.attack_hitbox.move(self.all_sprites.offset)
            #     pygame.draw.rect(self.display_surface, 'red', offset_hitbox, 2)
            #     offset_damage = self.player.damage_rect.move(self.all_sprites.offset)
            #     pygame.draw.rect(self.display_surface, 'green', offset_damage, 2)

            pygame.display.update()
        
        pygame.quit()
    
if __name__ == '__main__':
    game = Game()
    game.run()
    