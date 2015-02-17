__author__ = 'Curtis'
import os
import sys
import pygame
import game
import state


class DodgeGame():
    def __init__(self, size):
        self.size = size
        self.state_dict = None
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state_next
        #self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup()

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def start(self):
        x = game.GameScreenControl()
        x.main_loop()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Dodge Game")
    start = DodgeGame()
    start.start()
    pygame.quit()
    sys.exit()