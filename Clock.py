import pygame


class Clock:

    def __init__(self, fps):
        self.fps = fps
        self.clock = pygame.time.Clock()

    def get_dt(self):
        return self.clock.tick(self.fps)/1000