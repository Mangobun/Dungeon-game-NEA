from settings import *
from player import Player
from sprites import *
from groups import AllSprites
from support import scale_image, scale_pos
from ui import UI
from states import *
from database import Database

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
        
        self.game_state = 'menu'
        self.pause_start_time = 0
        self.player_name = ""

        self.load_audio()
        
        # states
        self.main_menu = MainMenu(self.display_surface, self.menu_click_sound, self.select_option_sound)
        self.instructions_screen = InstructionsScreen(self.display_surface)
        self.pause_menu = PauseMenu(self.display_surface, self.menu_click_sound, self.select_option_sound)
        self.game_over_screen = GameOverScreen(self.display_surface, self.menu_click_sound, self.select_option_sound)
        self.high_score_screen = HighScoreScreen(self.display_surface)

        # database
        self.database = Database()
        self.database.create_table()

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.pickup_sprites = pygame.sprite.Group()

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        self.enemy_spawn_interval = 1500
        pygame.time.set_timer(self.enemy_event, self.enemy_spawn_interval)
        self.spawn_positions = []
        
        # ui
        self.ui = UI()
        self.survival_score = 0
        self.enemy_score = 0
        self.total_score = 0
        self.score_start_time = pygame.time.get_ticks()

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

    def load_audio(self):
        # music
        self.background_music_path = join('audio', 'background music.mp3')
        self.normal_music_volume = 0.5
        self.paused_music_volume = 0.15

        # sound effects
        self.sword_swing_sound = pygame.mixer.Sound(join('audio', 'sword_swing.mp3'))
        self.damage_taken_sound = pygame.mixer.Sound(join('audio', 'damage_taken.mp3'))
        self.enemy_hit_sound = pygame.mixer.Sound(join('audio', 'enemy_sword_hit.mp3'))
        self.health_pickup_sound = pygame.mixer.Sound(join('audio', 'health_pickup.mp3'))
        self.menu_click_sound = pygame.mixer.Sound(join('audio', 'menu_click.mp3'))
        self.select_option_sound = pygame.mixer.Sound(join('audio', 'select_option.mp3'))
        self.game_start_sound = pygame.mixer.Sound(join('audio', 'game_start.mp3'))
        self.game_over_sound = pygame.mixer.Sound(join('audio', 'game_over.mp3'))

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
                self.player = Player((x, y), self.all_sprites, self.collision_sprites, self.sword_swing_sound)
            else:
                x, y = scale_pos(obj.x, obj.y)
                self.spawn_positions.append((x, y))

    def attack_collision(self):
        if self.player.attack_hitbox:
            for enemy in self.enemy_sprites:
                if enemy.death_time == 0 and enemy.hitbox_rect.colliderect(self.player.attack_hitbox):
                    self.enemy_hit_sound.play()
                    enemy.destroy()

                    if enemy.enemy_type == 'blob':
                        self.enemy_score += 25
                    elif enemy.enemy_type == 'bat':
                        self.enemy_score += 50

    def player_collision(self):
        if not self.player.attacking and not self.player.invincible:
            for enemy in self.enemy_sprites:
                if enemy.death_time == 0 and enemy.hitbox_rect.colliderect(self.player.damage_rect):
                    self.damage_taken_sound.play()

                    self.player.health = max(self.player.health - 1, 0)
                    self.player.invincible = True
                    self.player.damage_time = pygame.time.get_ticks()
                    break

    def pickup_collision(self):
        for pickup in self.pickup_sprites:
            if pickup.rect.colliderect(self.player.damage_rect):
                self.health_pickup_sound.play()

                self.player.health = min(self.player.health + 2, self.player.max_health)
                pickup.kill()

    def adjust_timers_after_pause(self, pause_duration):
        # survival score timer
        self.score_start_time += pause_duration

        # player attack timer
        if self.player.attacking:
            self.player.attack_time += pause_duration

        # player invincibility timer
        if self.player.invincible:
            self.player.damage_time += pause_duration

        # enemy death timers
        for enemy in self.enemy_sprites:
            if enemy.death_time != 0:
                enemy.death_time += pause_duration

        # heart pickup lifetime and flashing timers
        for pickup in self.pickup_sprites:
            pickup.spawn_time += pause_duration

    def reset_game(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.enemy_sprites.empty()
        self.pickup_sprites.empty()
        self.spawn_positions.clear()

        self.survival_score = 0
        self.enemy_score = 0
        self.total_score = 0
        self.score_start_time = pygame.time.get_ticks()

        pygame.time.set_timer(self.enemy_event, self.enemy_spawn_interval)

        self.setup()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    # main menu
                    if self.game_state == 'menu':
                        selected_option = self.main_menu.input(event)

                        if selected_option == 'Play':
                            self.game_state = 'instructions'

                        elif selected_option == 'High Scores':
                            self.high_score_screen.high_scores = self.database.get_high_scores()
                            self.game_state = 'high_scores'

                        elif selected_option == 'Exit':
                            self.running = False

                    # high score
                    elif self.game_state == 'high_scores':
                        if event.key == pygame.K_ESCAPE:
                            self.menu_click_sound.play()
                            self.game_state = 'menu'

                    # instruction screen
                    elif self.game_state == 'instructions':
                        start_game = self.instructions_screen.input(event)

                        if start_game:
                            self.player_name = self.instructions_screen.player_name.strip().title()
                            self.score_start_time = pygame.time.get_ticks()

                            self.game_start_sound.play()

                            self.game_state = 'playing'

                            pygame.mixer.music.load(self.background_music_path)
                            pygame.mixer.music.set_volume(self.normal_music_volume)
                            pygame.mixer.music.play(-1)

                    # escape to pause
                    elif self.game_state == 'playing':
                        if event.key == pygame.K_ESCAPE:
                            self.pause_start_time = pygame.time.get_ticks()
                            pygame.time.set_timer(self.enemy_event, 0)
                            self.pause_menu.selected_option = 0

                            pygame.mixer.music.set_volume(self.paused_music_volume)

                            self.game_state = 'paused'

                    # pause menu
                    elif self.game_state == 'paused':
                        selected_option = self.pause_menu.input(event)

                        if selected_option == 'Resume':
                            pause_duration = pygame.time.get_ticks() - self.pause_start_time

                            self.adjust_timers_after_pause(pause_duration)
                            pygame.time.set_timer(self.enemy_event, self.enemy_spawn_interval)

                            pygame.mixer.music.set_volume(self.normal_music_volume)

                            self.game_state = 'playing'

                        elif selected_option == 'Main Menu':
                            pygame.mixer.music.stop()
                            self.reset_game()
                            self.game_state = 'menu'

                    # game over
                    elif self.game_state == 'game_over':
                        selected_option = self.game_over_screen.input(event)

                        if selected_option == 'Retry':
                            self.game_over_sound.stop()
                            
                            self.reset_game()

                            self.game_start_sound.play()
                            
                            self.game_state = 'playing'

                            pygame.mixer.music.load(self.background_music_path)
                            pygame.mixer.music.set_volume(self.normal_music_volume)
                            pygame.mixer.music.play(-1)

                        elif selected_option == 'Main Menu':
                            self.game_over_sound.stop()
                            pygame.mixer.music.stop()
                            
                            self.reset_game()
                            self.game_state = 'menu'

                # enemy event
                if event.type == self.enemy_event and self.game_state == 'playing':
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

            if self.game_state == 'playing':
                # score time
                current_time = pygame.time.get_ticks()

                self.survival_score = (current_time - self.score_start_time) // 100
                self.total_score = self.survival_score + self.enemy_score

                # update
                self.all_sprites.update(dt)
                self.attack_collision()
                self.player_collision()

                if self.player.health <= 0:
                    self.database.add_score(self.player_name, self.total_score)

                    self.game_over_screen.score = self.total_score
                    self.game_over_screen.selected_option = 0

                    pygame.mixer.music.fadeout(800)
                    self.game_over_sound.play()

                    self.game_state = 'game_over'

                self.pickup_collision()

                # draw
                self.display_surface.fill(COLORS['background'])
                self.all_sprites.draw(self.player.rect.center)
                self.ui.display(self.player.health, self.total_score)

                # temporary hitbox visibility
                # if self.player.attack_hitbox:
                #     offset_hitbox = self.player.attack_hitbox.move(self.all_sprites.offset)
                #     pygame.draw.rect(self.display_surface, 'red', offset_hitbox, 2)
                #     offset_damage = self.player.damage_rect.move(self.all_sprites.offset)
                #     pygame.draw.rect(self.display_surface, 'green', offset_damage, 2)

            elif self.game_state == 'menu':
                self.main_menu.draw()

            elif self.game_state == "high_scores":
                self.high_score_screen.draw()

            elif self.game_state == 'instructions':
                self.instructions_screen.draw()

            elif self.game_state == 'paused':
                self.display_surface.fill(COLORS['background'])
                self.all_sprites.draw(self.player.rect.center)
                self.ui.display(self.player.health, self.total_score)

                self.pause_menu.draw()

            elif self.game_state == 'game_over':
                self.display_surface.fill(COLORS['background'])
                self.all_sprites.draw(self.player.rect.center)
                self.ui.display(self.player.health, self.total_score)

                self.game_over_screen.draw()

            pygame.display.update()
        
        pygame.quit()
    
if __name__ == '__main__':
    game = Game()
    game.run()
    