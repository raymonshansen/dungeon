"""Dungeon module."""

from random import randint

from map_mod import Map
from tiletypes import TileTypes
from message import MsgType


class Room():
    """A room in a dungeon. Holds info about as well as
    methods for interacting with a room while randomly constructing
    a level."""

    def __init__(self, left, top, width, height, level):
        """Constructor for room. The walls of the room is included in
        the given parameters."""
        if width < 3 or height < 3:
            raise AttributeError("Room too small!")
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.level = level
        self.floor = self.floor_tiles()
        self.walls = self.wall_tiles()
        self.all_tiles = self.floor + self.walls

    def overlap(self, room):
        """Return true if there are any tiles overlapping with the
        given room object. Checked by comparing coordinates as tile-types
        may change."""
        for tile in self.all_tiles:
            for comp_tile in room.all_tiles:
                if tile.coor == comp_tile.coor:
                    return True
        return False

    def wall_tiles(self):
        walllist = list()
        # Top and bottom row
        for x in range(self.left, self.left + self.width):
            walllist.append(self.level.get_tile(x, self.top))
            walllist.append(self.level.get_tile(x, self.top + self.height - 1))
        # Sides
        for y in range(self.top + 1, self.top + self.height - 1):
            walllist.append(self.level.get_tile(self.left, y))
            walllist.append(self.level.get_tile(self.left + self.width - 1, y))
        return walllist

    def floor_tiles(self):
        floorlist = list()
        for x in range(self.left + 1, self.left + self.width - 1):
            for y in range(self.top + 1, self.top + self.height - 1):
                floorlist.append(self.level.get_tile(x, y))
        return floorlist

    def set_floor_tiles(self):
        for tile in self.floor:
            tile.set_type(TileTypes.FLOOR)

    @property
    def floor_area(self):
        return (self.width - 2) * (self.height - 2)

    @property
    def total_area(self):
        return (self.width) * (self.height)


class Dungeon():
    """Dungeon class."""

    def __init__(self, surface, logview):
        """Contsructs a random map, items and monsters."""
        self.logview = logview
        self.screen = surface
        self.rooms = list()
        self.map = self.generate_dungeon()

    def generate_dungeon(self):
        level = Map(self.screen, self.logview, 50, 50)
        roomnum = randint(7, 17)
        maxtries = 100
        tries = 0
        self.logview.post("Roomnum: {}".format(roomnum), MsgType.INFO)
        self.logview.post("Maxtries: {}".format(maxtries), MsgType.INFO)

        while tries < maxtries and len(self.rooms) < roomnum:
            # Define a random room by its left, top, width and height
            width = randint(6, 10)
            height = randint(6, 10)
            left = randint(0, 49 - width)
            top = randint(0, 49 - height)
            room = Room(left, top, width, height, level)
            # Check placement
            good = True
            
            for existing_room in self.rooms:
                if room.overlap(existing_room):
                    good = False
            if good:
                room.set_floor_tiles()
                self.rooms.append(room)
            else:
                tries += 1
            print(tries)
            print(maxtries)

        self.logview.post("\n", MsgType.INFO)
        self.logview.post("Total rooms: {}".format(len(self.rooms)), MsgType.INFO)
        self.logview.post("Tries: {}".format(tries), MsgType.INFO)
        self.logview.post("\n", MsgType.INFO)

        return level

    def draw(self, screen, x, y):
        """Draws the map on the screen."""
        self.map.draw(screen, x, y)
