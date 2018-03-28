"""Tile module."""

import pygame
import os
# from random import randint

import constants as cons
from tiletypes import TileStatus


class Tile():
    """Tile class holds all information about a tile.

    A tile is the smallest unit of our map. Its types comes
    from a tilebank. It also knows about its own lighting via
    a separate pygame surface.
    """

    def __init__(self, x, y, bank):
        """Initialize the Tile class."""
        self.x = x
        self.y = y
        self.dim = cons.TILE_D
        self.types = bank
        self.type = None
        self.set_type(0)
        darkpath = os.path.join('tiles', 'dark.png')
        self.light = pygame.image.load(darkpath).convert()
        self.status = TileStatus.UNEXPLORED
        self.set_light(255)
        self.debugmark = False
        self.debugcol = None

    def __repr__(self):
        """Official string representation of a tile."""
        return f"({self.x},{self.y} - {self.get_type()})"

    def set_type(self, index):
        """Set the tile type based on a given index in its tile-bank."""
        self.type = index

    def set_status(self, status):
        """Set status of tile."""
        self.status = status

    def set_debug(self, col):
        self.debugmark = True
        self.debugcol = col

    def set_light(self, luminosity):
        """Set the tiles lighting based on a given value."""

        # Make sure already explored tiles never go completely dark again.
        if self.status == TileStatus.EXPLORED and luminosity == 255:
            self.light.set_alpha(230)
            return

        self.light.set_alpha(luminosity)

    def get_type(self):
        """Return the tiles type."""
        return self.type

    @property
    def is_see_through(self):
        """Return true if tile is see-through, else false."""
        return self.get_type() == 1

    def is_wall(self):
        """Return true if tile is wall, else false."""
        if 1 < self.get_type() <= 49:
            return True
        return False

    def is_floor(self):
        """Return true if tile is floor, else false."""
        if self.get_type() == 1:
            return True
        return False

    def is_none(self):
        """Return true if tile is floor, else false."""
        if self.get_type() == 0:
            return True
        return False

    def draw(self, surface, x, y):
        """Draw method.

        Calculate pixel placement, then blit the tile followed by its
        current lighting.
        """
        coor = (x * cons.TILE_D, y * cons.TILE_D)
        mid_coor = (x * cons.TILE_D + 16, y * cons.TILE_D + 16)

        if not self.is_wall():
            surface.blit(self.types.get_type(self.type), coor)
        else:
            wall = pygame.image.load('tiles2/wall49.png').convert()
            surface.blit(wall, coor)
        
        surface.blit(self.light, coor)
        if self.debugmark:
            pygame.draw.circle(surface, self.debugcol, mid_coor, 4)
