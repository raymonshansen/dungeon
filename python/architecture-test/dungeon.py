"""Dungeon module."""

from map_mod import Map
from typebank import TypeBank
from logview import MsgType


class Dungeon():
    """Dungeon class."""

    def __init__(self, surface, pos_rect, width, height, logview):
        """Contsructs a random map, items and monsters."""
        self.logview = logview
        self.typebank = TypeBank()
        self.logview.post("Loading map..", MsgType.INFO)
        self.map = Map(surface, pos_rect, self.typebank, 'testmap.txt')

    def draw(self, screen, x, y):
        """Draws the map on the screen."""
        self.map.draw(screen, x, y)
