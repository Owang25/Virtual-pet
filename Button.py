#button class for the game
import pygame

BUTTON_HOVER_COLOR = (0, 100, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 128, 255)
BUTTON_DISABLED_COLOR = (100, 100, 100)

# Button class
class Button:
    def __init__(self, text, action):
        self.text = text
        self.action = action
        self.rect = None
        self.enabled = True

    def draw(self, screen, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        mouse_pos = pygame.mouse.get_pos()
        if not self.enabled:
            color = BUTTON_DISABLED_COLOR
        elif self.rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if self.enabled and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect and self.rect.collidepoint(event.pos):
                self.action()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
