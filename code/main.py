from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from support import scale_image, scale_pos
from random import randint

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

        self.setup()   
        
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

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
           
            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(COLORS['background'])
            self.all_sprites.draw(self.player.rect.center)
            if self.player.attack_hitbox:
                offset_hitbox = self.player.attack_hitbox.move(self.all_sprites.offset)
                pygame.draw.rect(self.display_surface, 'red', offset_hitbox, 2)
            pygame.display.update()
        
        pygame.quit()
    
if __name__ == '__main__':
    game = Game()
    game.run()
    