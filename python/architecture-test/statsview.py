"""Stats module. Contains all classes and
methods needed to print the stats part of the game-window.
"""

import pygame as pg


class StatView():
    def __init__(self, surface, pos_rect):
        self.surface = surface
        self.topleft = pos_rect
        self.dirty = True

    def draw(self, screen):
        if self.dirty:
            self.surface.fill(pg.color.Color("black"))
            screen.blit(self.surface, self.topleft)
