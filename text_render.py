#text rendering function
import pygame
# Define a function to render text
def render_text(text, size, color, position):
    font = pygame.font.Font(None, size)
    screen = pygame.display.get_surface()
    
    # Split the text into multiple lines
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()

        if position[0] == 'center':
            position_x = (screen.get_width() - text_rect.width) // 2
        else:
            position_x = int(position[0])

        if position[1] == 'center':
            position_y = (screen.get_height() - text_rect.height) // 2 + i * text_rect.height
        else:
            position_y = int(position[1]) + i * text_rect.height

        screen.blit(text_surface, (position_x, position_y))