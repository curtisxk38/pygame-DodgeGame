__author__ = 'Curtis'
import state
import pygame
import button


class MenuScreenControl(state.State):
    def __init__(self):
        state.State.__init__(self)
        self.next = "game"
        self.button_list = []
        self.title_text = self.make_title_text()

    def go_to_game(self):
        self.next = "game"
        self.done = True

    def go_to_instructions(self):
        self.next = "instructions"
        self.done = True

    def go_to_scores(self):
        self.next = "scores"
        self.done = True

    def quit_game(self):
        self.quit = True

    def make_title_text(self):
        title_text = pygame.image.load("title_text.png").convert()
        title_rect = title_text.get_rect()
        title_rect.center = (pygame.display.get_surface().get_size()[0]/2, 150)
        return title_text, title_rect

    def make_buttons(self):
        rect = pygame.Rect(0, 0, 100, 20)
        rect.centerx = pygame.display.get_surface().get_size()[0]/2
        rect.centery = pygame.display.get_surface().get_size()[1]/2
        self.button_list.append(button.Button(rect, "Start", (0, 0, 0), 15, self.go_to_game))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Instructions", (0, 0, 0), 15, self.go_to_instructions))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Scores", (0, 0, 0), 15, self.go_to_scores))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Quit", (0, 0, 0), 15, self.quit_game))

    def startup(self):
        # if its empty
        if not self.button_list:
            self.make_buttons()

    def cleanup(self):
        pass

    def get_event(self, event):
        for b in self.button_list:
            b.get_event(event)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.quit = True

    def update(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(*self.title_text)
        for b in self.button_list:
            b.update(screen)
