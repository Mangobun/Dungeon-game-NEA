from settings import *

class MainMenu:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.title_font = pygame.font.Font(None, 80)
        self.text_font = pygame.font.Font(None, 40)
        

        self.options = ['Play', 'High Scores', 'Exit']
        self.selected_option = 0

    def draw(self):
        self.display_surface.fill(COLORS['background'])

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

        self.player_name = ""
        self.max_name_length = 12
    
    def draw(self):
            self.display_surface.fill(COLORS['background'])
            
            title = self.title_font.render("HOW TO PLAY", True, "white")
            title_rect = title.get_rect(center = (WINDOW_WIDTH // 2, 120))
            self.display_surface.blit(title, title_rect)

            name_label = self.text_font.render("Enter your name to begin:", True, "white")
            name_label_rect = name_label.get_rect(topleft = (180, 550))
            self.display_surface.blit(name_label, name_label_rect)
            
            input_rect = pygame.Rect(180, 585, 300, 40)
            pygame.draw.rect(self.display_surface, "white", input_rect, 2)  

            name_text = self.text_font.render(self.player_name, True, "white")
            name_text_rect = name_text.get_rect(midleft = (input_rect.left + 10, input_rect.centery))
            self.display_surface.blit(name_text, name_text_rect)

            instructions = [
                "WASD / Arrow Keys - Move",
                "Space - Attack",
                "Escape - Pause",
                "",
                "Defeat enemies and survive for as long as possible.",
                "Enemies may drop hearts when you have lost health."
            ]

            for index, instruction in enumerate(instructions):
                instruction_text = self.text_font.render(instruction, True, "white")
                instruction_rect = instruction_text.get_rect(topleft = (180, 210 + index * 50))
                self.display_surface.blit(instruction_text, instruction_rect)

    def input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]

        elif event.key == pygame.K_RETURN:
            if self.player_name:
                return True

        elif event.unicode.isprintable() and len(self.player_name) < self.max_name_length:
            self.player_name += event.unicode

        return False

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

        score_text = self.text_font.render(f"Score: {self.score:,}", True, "white")
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
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.title_font = pygame.font.Font(None, 70)
        self.text_font = pygame.font.Font(None, 40)

        self.high_scores = []

    def draw(self):
        self.display_surface.fill(COLORS['background'])

        title = self.title_font.render("HIGH SCORES", True, "white")
        title_rect = title.get_rect(center = (WINDOW_WIDTH // 2, 160))
        self.display_surface.blit(title, title_rect)

        if not self.high_scores:
            no_scores_text = self.text_font.render("No scores yet", True, "white")
            no_scores_rect = no_scores_text.get_rect(center = (WINDOW_WIDTH // 2, 230))
            self.display_surface.blit(no_scores_text, no_scores_rect)
        
        else:
            for index, (name, score) in enumerate(self.high_scores):
                score_text = self.text_font.render(f"{index + 1}: {name} - {score:,}", True, "white")
                score_rect = score_text.get_rect(center = (WINDOW_WIDTH // 2, 230 + index * 50))
                self.display_surface.blit(score_text, score_rect)

