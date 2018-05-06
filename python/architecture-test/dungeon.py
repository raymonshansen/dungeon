"""Dungeon module."""

from random import randint, choice

from map_mod import Map
from tiletypes import TileTypes
from message import MsgType
import constants as cons


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

    def overlap_tile(self, comptile):
        """Return true if there are any tiles overlapping with the
        given tile object. Checked by comparing coordinates as tile-types
        may change."""
        for tile in self.all_tiles:
            print(tile)
            print(comptile)
            if tile.coor == comptile.coor:
                return True
        return False

    def overlap_room(self, room):
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
        self.corridor_tiles = list()
        self.rooms = list()
        self.map = self.generate_dungeon()

    def generate_dungeon(self):
        """Wrapper for various stages of random generation."""
        level_with_rooms = self.generate_rooms()
        level_with_corridors = self.generate_corridors(level_with_rooms)
        return level_with_corridors

    def find_startingtile(self, level_with_rooms):
        startingtile = False
        while not startingtile:
            startingtile = choice(level_with_rooms.tiles)
            # Can't start digging inside the rooms!
            for room in self.rooms:
                overlap = False
                if room.overlap_tile(startingtile):
                    overlap = True
            if not overlap:
                x, y = startingtile.coor
                if not (x % 2) and not (y % 2):
                    startingtile = False
                else:
                    return startingtile

    def generate_corridors(self, level_with_rooms):
        start = self.find_startingtile(level_with_rooms)
        cells = list()
        cells.append(start)
        while cells:
            current = choice(cells)
            current.set_type(TileTypes.FLOOR)
            self.corridor_tiles.append(current)
            one_step_valid = list()
            two_step_valid = list()
            for key in cons.FOUR_DIRECTIONS:
                tup = cons.FOUR_DIRECTIONS.get(key)
                x, y = current.coor
                neig = level_with_rooms.get_tile_neighbour(x, y, tup, 2)
                if not neig:
                    # Abort if we go off the map!
                    break
                elif neig.get_type() == TileTypes.WALL:
                    one_step_valid.append(neig)
                    neig2 = level_with_rooms.get_tile_neighbour(x, y, tup)
                    if neig2 and neig2.get_type() == TileTypes.WALL:
                        two_step_valid.append(neig2)
            if not one_step_valid:
                cells.remove(current)
            else:
                idx = randint(0, len(one_step_valid)-1)
                one_step_valid[idx].set_type(TileTypes.FLOOR)
                two_step_valid[idx].set_type(TileTypes.FLOOR)
                self.corridor_tiles.append(two_step_valid[idx])
                cells.append(one_step_valid[idx])

        return level_with_rooms

    def randint_odd(self, start, stop):
        num = randint(start, stop)
        while not num % 2:
            num = randint(start, stop)
        return num

    def randint_even(self, start, stop):
        num = randint(start, stop)
        while num % 2:
            num = randint(start, stop)
        return num

    def generate_rooms(self):
        level_with_rooms = Map(self.screen, self.logview, 63, 63)
        roomnum = randint(7, 17)
        maxtries = 100
        tries = 0
        self.logview.post("Roomnum: {}".format(roomnum), MsgType.INFO)
        self.logview.post("Maxtries: {}".format(maxtries), MsgType.INFO)

        while tries < maxtries and len(self.rooms) < roomnum:
            # Could move these into the Room-class, but might
            # want to fiddle with them later...
            width = self.randint_odd(6, 10)
            height = self.randint_odd(6, 10)
            left = self.randint_even(0, 49 - width)
            top = self.randint_even(0, 49 - height)
            while left <= 1 or top <= 1:
                left = self.randint_even(0, 49 - width)
                top = self.randint_even(0, 49 - height)

            room = Room(left, top, width, height, level_with_rooms)
            good = True
            for existing_room in self.rooms:
                if room.overlap_room(existing_room):
                    good = False
            if good:
                room.set_floor_tiles()
                self.rooms.append(room)
                self.logview.post("Room nr: {}. left: {} top: {} width: {} height: {}".format(len(self.rooms), room.left, room.top, room.width, room.height), MsgType.DEBUG)
            tries += 1

        # Print the results to the logviewer.
        self.logview.post("\n", MsgType.INFO)
        self.logview.post("Total rooms: {}".format(len(self.rooms)), MsgType.INFO)
        self.logview.post("Tries: {}".format(tries), MsgType.INFO)
        self.logview.post("\n", MsgType.INFO)

        return level_with_rooms

    def draw(self, screen, x, y):
        """Draws the map on the screen."""
        self.map.draw(screen, x, y)
