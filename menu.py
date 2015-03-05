__author__ = 'Curtis'
import state
import pygame
import button


class MenuScreenControl(state.State):
    def __init__(self):
        state.State.__init__(self)
        self.next = "game"
        self.button_list = []

    def finish_menu(self):
        self.done = True

    def quit_game(self):
        self.quit = True

    def make_buttons(self):
        rect = pygame.Rect(0, 0, 80, 20)
        rect.centerx = pygame.display.get_surface().get_size()[0]/2
        rect.centery = pygame.display.get_surface().get_size()[1]/2
        self.button_list.append(button.Button(rect, "Start", (0, 0, 0), 15, self.finish_menu))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Controls", (0, 0, 0), 15, None))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Quit", (0, 0, 0), 15, self.quit_game))


    def startup(self):
        self.make_buttons()

    def cleanup(self):
        self.button_list = []

    def get_event(self, event):
        for b in self.button_list:
            b.get_event(event)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.quit = True

    def update(self, screen, dt):
        self.draw(screen)
        for b in self.button_list:
            b.update(screen)

    def draw(self, screen):
        screen.fill((255, 255, 255))

