__author__ = 'Curtis'
import os
import sys
import pygame
import game
import menu
import scores


class DodgeGame():
    def __init__(self, size, fps):
        self.size = size
        self.fps = fps
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.game_done = False

        self.state_dict = None
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        # before doing anything else, get score from game state, and send to scores state
        # probably a better way to do this
        if previous == "game":
            self.state_dict[self.state_name].receive_recent_score(self.state_dict[previous].hold_score)
        self.state.startup()
        self.state.previous = previous


    def update(self, dt):
        if self.state.quit:
            self.game_done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_done = True
            self.state.get_event(event)

    def main_loop(self):
        while not self.game_done:
            time_delta = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(time_delta)
            pygame.display.update()


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Dodge Game")

    screen_size = (720, 480)
    screen_fps = 60.0
    start = DodgeGame(screen_size, screen_fps)

    state_dict = {'menu': menu.MenuScreenControl(),
                  'game': game.GameScreenControl(),
                  # 'instructions': todo
                  'scores': scores.ScoresScreenControl()
    }
    start.setup_states(state_dict, 'menu')
    start.main_loop()
    pygame.quit()
    sys.exit()