import pygame as pg
# Needed globals
from config import TILESIZE
from config import Point
from config import colors

"""
Tiles represent the smallest unit of area in
the dungeon. The starting space is reduced to
a two-dimentional list of tiles to represent any
point.

A tile can be dug or filled.
"""


class Tile():
    """Class to manage tiles."""
    def __init__(self, x, y, regionid, wallimage, floorimage, vertdoor, hordoor, dug=False):
        """Constructor for tiles."""
        self.wall_image = wallimage
        self.floor_image = floorimage
        self.door_image = vertdoor
        self.hor_door = hordoor
        self.pos = Point(x, y)
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.id = regionid
        self.color = colors[self.id % len(colors)]
        self.dug = dug
        self.roomid = None
        self.corridor = False
        self.is_mapped = False
        self.is_digable = True
        self.is_door = False
        self.is_wall = True
        self.space = False

    def __repr__(self):
        """Who are you?"""
        return "<{name} at {pos.x}, {pos.y}>".format(name=self.__class__.__name__, pos=self.pos)

    @property
    def center(self):
        return Point(self.pos.x+(TILESIZE/2), self.pos.y+(TILESIZE/2))

    def carve(self, screen):
        self.dug = True
        self.is_wall = False
        self.corridor = True
        self.dug = True
        self.draw_tile(screen)
        pg.display.update()

    def draw_tile(self, screen):
        if self.is_wall:
            screen.blit(self.wall_image, self.rect)
        if self.dug:
            screen.blit(self.floor_image, self.rect)
            pg.draw.rect(screen, colors[self.id % len(colors)], self.rect, 1)
        if self.is_door:
            screen.blit(self.door_image, self.rect)
        if self.corridor:
            screen.blit(self.floor_image, self.rect)
            pg.draw.rect(screen, pg.color.THECOLORS["white"], self.rect, 1)
