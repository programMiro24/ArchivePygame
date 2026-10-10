import pygame
import sys

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Center v2.0 - Python игри 3")
clock = pygame.time.Clock()

# color
BLACK = (20, 20, 30)
WHITE = (240, 240, 240)
GREEN = (0, 255, 127)
YELLOW = (255, 215, 0)
GRAY = (120, 120, 140)

class GameMenu:  #class control main menu
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 32)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.games=[
            "1. Classic Snake",
            "2. Angry Birds",
            "3. Space Invaders",
            "4. Platformer - Jump & Run [Ново]",
            "5. Arkanoid [Ново]",
            "6. Zombie Survival Lab [Ново]",
            "ESC. Изход"
        ]
        self.selected_index = 0
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.games)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.games)
            elif event.key == pygame.K_RETURN:
                return self.selected_index
        return None
    def draw(self, surface):
        surface.fill(BLACK)
        title_surf = self.title_font.render("Game Center v2.0", True, YELLOW)
        surface.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 40))
        for i, option in enumerate(self.games):
            color = GREEN if i == self.selected_index else GRAY
            if "[Ново]" in option and i != self.selected_index:
                color = (200, 100, 255)

            opt_surf = self.font.render(option, True, color)
            surface.blit(opt_surf, (100, 130+i*50))
            
