import pygame
import state
import button
import pickle

BLACK = (0, 0, 0)

class ScoresScreenControl(state.State):
    def __init__(self):
        state.State.__init__(self)
        self.next = "menu"
        self.recent_score = None
        rect = pygame.Rect(0, 0, 80, 20)
        rect.centerx, rect.centery = pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]-60
        self.menu_button = button.Button(rect, "Menu", (0, 0, 0), 15, self.finish)
        self.font = pygame.font.Font('freesansbold.ttf', 30)

        self.score_board = None

    def receive_recent_score(self, score):
        self.recent_score = score

    def update_score_board(self):
        """Precondition: self.text is not None"""
        self.score_board.append(self.recent_score)
        # sort score_board, largest to smallest
        self.score_board.sort(reverse=True)
        if len(self.score_board) > 10:
            # if score_board has more than 10 entries, trim of the lower values to make it have 10 entries
            self.score_board = self.score_board[:10]

    def make_game_over_text(self):
        """Precondition: self.text is not None"""
        self.text = self.font.render("Game Over! Your score was %s!" % self.recent_score, True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (pygame.display.get_surface().get_size()[0]/2, 50)



    def finish(self):
        self.done = True

    def startup(self):
        try:
            self.score_board = pickle.load(open("scoreboard.pkl", "rb"))
        except FileNotFoundError:
            self.score_board = []

        if self.recent_score is not None:
            self.update_score_board()
            self.make_game_over_text()




    def cleanup(self):
        pickle.dump(self.score_board, open("scoreboard.pkl", "wb"))
        self.recent_score = None

    def get_event(self, event):
        self.menu_button.get_event(event)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.done = True

    def update(self, screen, dt):
        screen.fill((255, 255, 255))
        if self.recent_score is not None:
            screen.blit(self.text, self.text_rect)
        self.menu_button.update(screen)
