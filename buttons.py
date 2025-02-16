import pygame


class Button:

    def __init__(self, text, pos, width, height) -> None:
        self.x, self.y = pos
        self.button_width = width
        self.button_height = height
        self.message = text

        self.font = pygame.font.Font(None, 24)
        self.button_surface = pygame.Surface((self.button_width, self.button_height))
        self.button_surface.fill('light blue')
        self.text = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.button_width / 2, self.button_height / 2))
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, window):
        window.blit(self.button_surface, (self.x, self.y))
        window.blit(self.text, (self.x + self.text_rect.x, self.y + self.text_rect.y))
        pygame.draw.rect(window, (0, 0, 0), self.rect, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class LevelButton(Button):
    
    def __init__(self, level, pos, width, height):
        super().__init__(level, pos, width, height)
        self.level = self.message
    
class NewGameButton(Button):

    def __init__(self, pos, width, height):
        super().__init__('New Game', pos, width, height)

class SolveButton(Button):

    def __init__(self, pos, width, height):
        super().__init__('Solve', pos, width, height)