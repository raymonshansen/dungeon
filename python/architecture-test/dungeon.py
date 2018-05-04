"""Dungeon module."""

from map_mod import Map


class Dungeon():
    """Dungeon class."""

    def __init__(self, surface, pos_rect, logview):
        """Contsructs a random map, items and monsters."""
        self.logview = logview
        self.map = Map(surface, pos_rect, 'map-tiny.txt', logview)

    def draw(self, screen, x, y):
        """Draws the map on the screen."""
        self.map.draw(screen, x, y)
