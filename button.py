import pygame


class Button():
    def __init__(self, rect, text, color, size, function):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.function = function
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.render_text()

    def render_text(self):
        if self.text is not None:
            self.text = self.font.render(self.text, True, self.color)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.function()

    def update(self, surface):
        pygame.draw.rect(surface, (0,0,0), self.rect, 1)
        surface.blit(self.text, self.rect)
