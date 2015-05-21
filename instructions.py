import pygame
import state
import button

class InstructionsScreenControl(state.State):
    def __init__(self):
        state.State.__init__(self)
        self.next = "menu"
        self.menu_button = self.make_menu_button()
        self.KEY_BINDINGS = {"LEFT": pygame.K_LEFT,
                "RIGHT": pygame.K_RIGHT}

    def make_menu_button(self):
        rect = pygame.Rect(0, 0, 80, 20)
        rect.centerx, rect.centery = pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]-60
        my_button = button.Button(rect, "Menu", (0, 0, 0), 15, self.finish)
        return my_button

    def finish(self):
        self.done = True

    def startup(self):
        pass

    def cleanup(self):
        pass

    def get_event(self, event):
        self.menu_button.get_event(event)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.done = True

    def update(self, screen, dt):
        screen.fill((255, 255, 255))
        self.menu_button.update(screen)
