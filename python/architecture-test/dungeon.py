"""Dungeon module."""

from random import randint

from map_mod import Map
from tiletypes import TileTypes
from message import MsgType


class Dungeon():
    """Dungeon class."""

    def __init__(self, surface, logview):
        """Contsructs a random map, items and monsters."""
        self.logview = logview
        self.screen = surface
        self.map = self.generate_dungeon()

    def generate_dungeon(self):
        level = Map(self.screen, self.logview, 50, 50)
        roomnum = randint(20, 30)
        maxtries = 200
        tries = 0
        self.logview.post("Roomnum: {}".format(roomnum), MsgType.DEBUG)
        self.logview.post("Maxtries: {}".format(maxtries), MsgType.DEBUG)
        placed_rooms = 0
        while placed_rooms < roomnum or tries < maxtries:
            # Define a random room by its left, top, width and height
            width = randint(5, 20)
            height = randint(5, 20)
            left = randint(2, 49 - width)
            top = randint(2, 49 - height)
            # Check placement
            good = True
            for x in range(left-1, left + width + 1):
                for y in range(top-1, top + height + 1):
                    if level.get_type(x, y) == TileTypes.FLOOR:
                        good = False
                        break
            # Place room, or not...
            if good:
                for x in range(left, left + width):
                    for y in range(top, top + height):
                        level.set_type(x, y, TileTypes.FLOOR)
                placed_rooms += 1
            else:
                tries += 1
            if tries > maxtries:
                break
        return level

    def draw(self, screen, x, y):
        """Draws the map on the screen."""
        self.map.draw(screen, x, y)
