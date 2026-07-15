from settings import *

class MainMenu:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.title_font = pygame.font.Font(None, 80)
        self.text_font = pygame.font.Font(None, 40)
        

        self.options = ['Play', 'High Scores', 'Exit']
        self.selected_option = 0

    def draw(self):
        self.display_surface.fill("black")

        title = self.title_font.render("Dungeon Game", True, "white")
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.display_surface.blit(title, title_rect)

        for index, option in enumerate(self.options):
            option_text = self.text_font.render(option, True, "white")
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + (index * 50)))
            self.display_surface.blit(option_text, option_rect)

            if index == self.selected_option:
                arrow = self.text_font.render(">", True, "white")
                arrow_rect = arrow.get_rect(midright = (option_rect.left - 10, option_rect.centery - 4))
                self.display_surface.blit(arrow, arrow_rect)
        
    def input(self, event):
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.selected_option += 1
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.selected_option -= 1

        self.selected_option %= len(self.options)

        if event.key == pygame.K_RETURN:
            return self.options[self.selected_option]

class InstructionsScreen:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.title_font = pygame.font.Font(None, 70)
        self.text_font = pygame.font.Font(None, 40)
    
    def draw(self):
            self.display_surface.fill("black")
            
            title = self.title_font.render("HOW TO PLAY", True, "white")
            title_rect = title.get_rect(center = (WINDOW_WIDTH // 2, 120))
            self.display_surface.blit(title, title_rect)

            instructions = [
                "WASD / Arrow Keys - Move",
                "Space - Attack",
                "Escape - Pause",
                "",
                "Defeat enemies and survive for as long as possible.",
                "Enemies may drop hearts when you have lost health.",
                "",
                "Press 'Enter' to Begin"
            ]

            for index, instruction in enumerate(instructions):
                instruction_text = self.text_font.render(instruction, True, "white")
                instruction_rect = instruction_text.get_rect(topleft = (180, 230 + index * 50))
                self.display_surface.blit(instruction_text, instruction_rect)

    def input(self, event):
        if event.key == pygame.K_RETURN:
            return True

class PauseMenu:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.title_font = pygame.font.Font(None, 70)
        self.text_font = pygame.font.Font(None, 40)

        self.options = ['Resume', 'Main Menu']
        self.selected_option = 0

    def draw(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.display_surface.blit(overlay, (0, 0))

        title = self.title_font.render("PAUSED", True, "white")
        title_rect = title.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        self.display_surface.blit(title, title_rect)

        for index, option in enumerate(self.options):

            option_text = self.text_font.render(option, True, "white")
            option_rect = option_text.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + (index * 50)))
            self.display_surface.blit(option_text, option_rect)

            if index == self.selected_option:
                arrow = self.text_font.render(">", True, "white")
                arrow_rect = arrow.get_rect(midright=(option_rect.left - 10, option_rect.centery - 4))
                self.display_surface.blit(arrow, arrow_rect)

    def input(self, event):
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.selected_option += 1
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.selected_option -= 1

        self.selected_option %= len(self.options)

        if event.key == pygame.K_RETURN:
            return self.options[self.selected_option]

class GameOverScreen:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.title_font = pygame.font.Font(None, 80)
        self.text_font = pygame.font.Font(None, 40)

        self.options = ['Retry', 'Main Menu']
        self.selected_option = 0

        self.score = 0

    def draw(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((120, 0, 0, 150))
        self.display_surface.blit(overlay, (0, 0))

        title = self.title_font.render("GAME OVER", True, "white")
        title_rect = title.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.display_surface.blit(title, title_rect)

        score_text = self.text_font.render(f"Score: {self.score}", True, "white")
        score_rect = score_text.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.display_surface.blit(score_text, score_rect)

        for index, option in enumerate(self.options):
            option_text = self.text_font.render(option, True, "white")
            option_rect = option_text.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20 + index * 40))
            self.display_surface.blit(option_text, option_rect)

            if index == self.selected_option:
                arrow = self.text_font.render(">", True, "white")
                arrow_rect = arrow.get_rect(midright = (option_rect.left - 10, option_rect.centery - 4))
                self.display_surface.blit(arrow, arrow_rect)

    def input(self, event):
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.selected_option += 1
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.selected_option -= 1

        self.selected_option %= len(self.options)

        if event.key == pygame.K_RETURN:
            return self.options[self.selected_option]

class HighScoreScreen:
    pass
