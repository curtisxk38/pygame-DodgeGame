

class State():
    def __init__(self):
        self.done = False #done will cause the program to move onto the next state
        self.next = None
        self.quit = False #quit causes whole program to quit
        self.previous = None
