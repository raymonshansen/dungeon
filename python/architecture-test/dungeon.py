"""Dungeon module."""

from map_mod import Map
from dungeon_generator import generate_dungeon


class Dungeon():
    """Dungeon class."""

    def __init__(self, surface, logview):
        """Contsructs a random map, items and monsters."""
        self.logview = logview
        self.screen = surface
        self.corridor_tiles = list()
        self.rooms = list()
        self.map = Map(self.screen, self.logview, 33, 33)
        generate_dungeon(self)

    def draw(self, screen, x, y):
        """Draws the map on the screen."""
        self.map.draw(screen, x, y)
