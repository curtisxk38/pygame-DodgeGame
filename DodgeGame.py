__author__ = 'Curtis'

import os
import sys
import pygame
import vector
import math
import random

SCREEN_SIZE = (720, 480)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 102, 0)
TRANSPARENT = (0, 0, 0, 0)

COLOR_KEY = (255, 0, 255)

KEY_BINDINGS = {"LEFT": pygame.K_LEFT,
                "RIGHT": pygame.K_RIGHT}

DIRECT_DICT = {KEY_BINDINGS["LEFT"]: vector.Vector(-2, 0),
               KEY_BINDINGS["RIGHT"]: vector.Vector(2, 0)}

things = pygame.sprite.Group()

score = [0]


class Player(pygame.sprite.Sprite):
    def __init__(self, speed, rect):
        self.rect = pygame.Rect(rect)
        self.move = vector.Vector(self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.life = 5
        self.boundary_rect = pygame.Rect(50, 0, SCREEN_SIZE[0] - 50, SCREEN_SIZE[1])

        self.direction = KEY_BINDINGS["RIGHT"]
        self.old_direction = None
        self.redraw = False
        self.image = None
        self.frame = 0
        self.frames = self.get_frames()
        self.animate_timer = 0.0
        self.animate_fps = 8.0
        self.walk_frames = []
        self.walk_frame_dict = self.make_frame_dict()
        self.adjust_images()

    def get_frames(self):
        #Get a list of all frames
        sheet = PLAYER_IMAGE
        indices = [[0,0], [1,0], [2,0]]
        return get_images(sheet, indices, self.rect.size)

    def make_frame_dict(self):
        #Create a dictionary of direction keys to frames
        #Use transform functions to reduce the size of the sprite sheet used
        frames = {None : [self.frames[0]],
                  KEY_BINDINGS["LEFT"] : [self.frames[1],
                                          self.frames[2]],
                  KEY_BINDINGS["RIGHT"]: [pygame.transform.flip(self.frames[1], True, False),
                                          pygame.transform.flip(self.frames[2], True, False)]}
        return frames

    def adjust_images(self):
        if self.direction != self.old_direction:
            self.walk_frames = self.walk_frame_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image()

    def make_image(self):
        #Update animation as needed
        now = pygame.time.get_ticks()
        if self.redraw or now - self.animate_timer > 1000/self.animate_fps:
            if self.direction is not None:
                self.frame = (self.frame + 1) % (len(self.walk_frames))
                self.image = self.walk_frames[self.frame]
            else:
                self.image = self.frames[0]
            self.animate_timer = now
        if not self.image:
            self.image = self.walk_frames[self.frame]
        self.redraw = False

    def change_direction(self, pos_change):
        if pos_change.x > 0:
            self.direction = KEY_BINDINGS["RIGHT"]
        elif pos_change.x < 0:
            self.direction = KEY_BINDINGS["LEFT"]
        elif pos_change.x == 0:
            self.direction = None

    def update(self, pressed_keys, dt):
        change = vector.Vector(0, 0)
        for key in DIRECT_DICT:
            if pressed_keys[key]:
                change.add_vector(DIRECT_DICT[key])
        self.change_direction(change)
        #print(self.direction)
        frame_speed = self.speed * dt
        change.multiply_by_scalar(frame_speed)
        self.move.add_vector(change)
        self.rect.center = self.move.x, self.move.y

        if not self.boundary_rect.contains(self.rect):
            self.rect.clamp_ip(self.boundary_rect)
            self.move = vector.Vector(self.rect.centerx, self.rect.centery)
        self.adjust_images()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, speed, angle, rect):
        pygame.sprite.Sprite.__init__(self, things)
        self.speed = speed
        self.rect = pygame.Rect(rect)
        self.velocity = vector.Vector(self.speed*math.cos(angle), self.speed*math.sin(angle))
        self.move = vector.Vector(self.rect.centerx, self.rect.centery)
        self.image = self.make_image()
        self.BOUNCE_LOSS = 1.5

    def make_image(self):
        image = pygame.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pygame.draw.ellipse(image, BLACK, image_rect)
        pygame.draw.ellipse(image, ORANGE, image_rect.inflate(-2, -2))
        return image

    def update(self, dt):
        self.velocity.add_vector(vector.Vector(0, .8))
        change = self.velocity
        frame_speed = 60 * dt
        change.multiply_by_scalar(frame_speed)
        self.move.add_vector(change)
        self.rect.center = self.move.x, self.move.y
        for thingy in things:
            if isinstance(thingy, Wall):
                if self.rect.bottom >= thingy.rect.top:
                    self.rect.bottom = thingy.rect.top
                    self.velocity.y = -self.velocity.y + self.BOUNCE_LOSS
                    self.move = vector.Vector(self.rect.centerx, self.rect.centery)
        if self.rect.left > SCREEN_SIZE[0]:
            pygame.sprite.Sprite.kill(self)
            score[0] += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Wall(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self, things)
        self.rect = pygame.Rect(rect)
        self.image = self.make_image()

    def make_image(self):
        image = pygame.Surface(self.rect.size).convert_alpha()
        image.fill(BLACK)
        return image

    def update(self, nothing_to_see_here):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Text():
    def __init__(self, text, size, color, pos):
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.color = color
        self.text = self.font.render(text, 1, color)
        self.pos = pos

    def draw(self, surface):
        surface.blit(self.text, self.pos)

    def update(self, text_to_render):
        self.text = self.font.render(text_to_render, 1, self.color)


class Control():
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.CLOCK = pygame.time.Clock()
        self.fps = 60.0
        self.running = True
        self.pressed_keys = pygame.key.get_pressed()
        self.player = self.make_player()
        self.make_walls()
        self.score_text = self.make_score_text()

    def make_player(self):
        player = Player(200, (0, 0, 16, 32))
        player.move.y = SCREEN_SIZE[1] - player.rect.height/2 - 50
        return player

    def make_walls(self):
        Wall((0, SCREEN_SIZE[1] - 50, SCREEN_SIZE[0], 10))

    def make_balls(self, timer):
        now = pygame.time.get_ticks()
        if now - timer >= 600:
            speed = random.random() * 5.0 + 4
            angle = random.random() * 10 * math.pi / 12.0 - 5.0*math.pi/12.0
            Ball(speed, angle, (-10, 0, 15, 15,))
            return now
        return timer

    def make_score_text(self):
        text = Text(str(score[0]), 20, BLACK, (0, 460))
        return text

    def event_loop(self):
        for event in pygame.event.get():
            self.pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.pressed_keys[pygame.K_ESCAPE]:
                self.running = False

    def main_loop(self):
        ball_timer = pygame.time.get_ticks()
        while self.running:
            time_delta = self.CLOCK.tick(self.fps)/1000.0
            self.event_loop()
            ball_timer = self.make_balls(ball_timer)
            self.player.update(self.pressed_keys, time_delta)
            things.update(time_delta)
            self.score_text.update(str(score[0]))
            self.screen.fill(WHITE)
            things.draw(self.screen)
            self.score_text.draw(self.screen)
            self.player.draw(self.screen)
            pygame.display.update()


def get_images(sheet, frame_indices, size):
    frames = []
    for cell in frame_indices:
        frame_rect = ((size[0]*cell[0], size[1] * cell[1]), size)
        frames.append(sheet.subsurface(frame_rect))
    return frames

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_caption("Dodge Game")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    PLAYER_IMAGE = pygame.image.load("sprite_sheet.png").convert()
    PLAYER_IMAGE.set_colorkey(COLOR_KEY)
    run = Control()
    run.main_loop()
    pygame.quit()
    sys.exit()