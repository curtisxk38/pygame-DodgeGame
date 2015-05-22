import pygame
import state
import button
import pickle

BLACK = (0,0,0)


class InstructionsScreenControl(state.State):
    def __init__(self):
        state.State.__init__(self)
        self.next = "menu"
        self.buttonlist = [self.make_menu_button()]
        self.key_bindings = None
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = []
        self.pressed_keys = None

        self.waiting_for_key = False
        self.pressed_button_index = 1

    def make_menu_button(self):
        rect = pygame.Rect(0, 0, 80, 20)
        rect.centerx, rect.centery = pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]-60
        my_button = button.Button(rect, "Menu", BLACK, 15, self.finish)
        return my_button

    def make_text(self):
        left = self.font.render("Move Left: ", True, BLACK)
        left_rect = left.get_rect()
        left_rect.topleft = (40, 200)
        self.text.append((left, left_rect))

        right = self.font.render("Move Right: ", True, BLACK)
        right_rect = right.get_rect()
        right_rect.topleft = (40, 240)
        self.text.append((right, right_rect))

    def new_left_key_function(self):
        if not self.waiting_for_key:
            self.waiting_for_key = True
            self.pressed_button_index = 1
            self.buttonlist[1].text = "___"
            self.buttonlist[1].render_text()
        else:
            self.waiting_for_key = False
            self.buttonlist[1].text = pygame.key.name(self.key_bindings["LEFT"])
            self.buttonlist[1].render_text()

    def new_right_key_function(self):
        if not self.waiting_for_key:
            self.waiting_for_key = True
            self.pressed_button_index = 2
            self.buttonlist[2].text = "___"
            self.buttonlist[2].render_text()
        else:
            self.waiting_for_key = False
            self.buttonlist[2].text = pygame.key.name(self.key_bindings["RIGHT"])
            self.buttonlist[2].render_text()

    def bind_key(self, key):
        if self.pressed_button_index == 1:
            self.key_bindings["LEFT"] = key
            self.new_left_key_function()
        elif self.pressed_button_index == 2:
            self.key_bindings["RIGHT"] = key
            self.new_right_key_function()

    def make_key_buttons(self):
        left_rect = pygame.Rect(0, 0, 60, 20)
        left_rect.topleft = (180, 200)
        self.buttonlist.append(button.Button(left_rect, pygame.key.name(self.key_bindings["LEFT"]), BLACK, 15, self.new_left_key_function))

        right_rect = pygame.Rect(0, 0, 60, 20)
        right_rect.topleft = (180, 240)
        self.buttonlist.append(button.Button(right_rect, pygame.key.name(self.key_bindings["RIGHT"]), BLACK, 15, self.new_right_key_function))

    def load_keybindings(self):
        try:
            self.key_bindings = pickle.load(open("keybindings.pkl", "rb"))
        except FileNotFoundError:
            self.key_bindings = {"LEFT": pygame.K_LEFT,
                "RIGHT": pygame.K_RIGHT}

    def finish(self):
        self.done = True

    def startup(self):
        self.load_keybindings()
        if not self.text:
            self.make_text()
        if len(self.buttonlist) < 3:
            self.make_key_buttons()

    def cleanup(self):
        pickle.dump(self.key_bindings, open("keybindings.pkl", "wb"))

    def get_event(self, event):
        self.pressed_keys = pygame.key.get_pressed()
        for button in self.buttonlist:
            button.get_event(event)
        if self.pressed_keys[pygame.K_ESCAPE]:
            self.done = True
        if self.waiting_for_key and event.type == pygame.KEYDOWN:
            self.bind_key(event.key)



    def update(self, screen, dt):
        screen.fill((255, 255, 255))
        for button in self.buttonlist:
            button.update(screen)
        for i in self.text:
            screen.blit(*i)
