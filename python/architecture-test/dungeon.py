"""Dungeon module."""

from random import randint, choice, sample

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
        self.doors = list()
        self.floor = self.floor_tiles()
        self.walls = self.wall_tiles()
        self.all_tiles = self.floor + self.walls

    def overlap_tile(self, comptile):
        """Return true if there are any tiles overlapping with the
        given tile object. Checked by comparing coordinates as tile-types
        may change."""
        for tile in self.all_tiles:
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

    def get_top_wall(self):
        wallist = list()
        for x in range(self.left+1, self.left + self.width-1):
            wallist.append(self.level.get_tile(x, self.top))
        return wallist

    def get_bottom_wall(self):
        wallist = list()
        for x in range(self.left+1, self.left + self.width-1):
            wallist.append(self.level.get_tile(x, self.top + self.height - 1))
        return wallist

    def get_left_wall(self):
        wallist = list()
        for y in range(self.top + 1, self.top + self.height - 1):
            wallist.append(self.level.get_tile(self.left, y))
        return wallist

    def get_right_wall(self):
        wallist = list()
        for y in range(self.top + 1, self.top + self.height - 1):
            wallist.append(self.level.get_tile(self.left + self.width - 1, y))
        return wallist

    def get_corner_wall(self):
        wallist = list()
        wallist.append(self.level.get_tile(self.left, self.top))
        wallist.append(self.level.get_tile(self.left, self.top + self.height - 1))
        wallist.append(self.level.get_tile(self.left + self.width - 1, self.top))
        wallist.append(self.level.get_tile(self.left + self.width - 1, self.top + self.height - 1))
        return wallist

    def random_tile_from_list(self, tiles, tilenum):
        return sample(tiles, tilenum)

    def wall_tiles(self):
        wallist = list()
        north = self.get_top_wall()
        wallist += north
        self.doors += self.random_tile_from_list(north, randint(1, 3))
        south = self.get_bottom_wall()
        wallist += south
        self.doors += self.random_tile_from_list(south, randint(1, 3))
        west = self.get_left_wall()
        wallist += west
        self.doors += self.random_tile_from_list(west, randint(1, 3))
        east = self.get_right_wall()
        wallist += east
        self.doors += self.random_tile_from_list(east, randint(1, 3))
        corners = self.get_corner_wall()
        wallist += corners
        return wallist

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
        self.startingtile = None
        self.map = self.generate_dungeon()

    def get_starting_coor(self):
        return self.startingtile.coor

    def generate_dungeon(self):
        """Wrapper for various stages of random generation."""
        level_with_rooms = self.generate_rooms()
        level_with_corridors = self.generate_corridors(level_with_rooms)
        self.generate_doors(level_with_corridors)
        self.remove_dead_ends(level_with_corridors)
        return level_with_corridors

    def is_dead_end(self, tile, level):
        """Return true if tile is a dead end."""
        x, y = tile.coor
        i = 0
        for _, tup in cons.FOUR_DIRECTIONS.items():
            neighbour = level.get_tile_neighbour(x, y, tup, 1)
            if neighbour.get_type() == TileTypes.FLOOR:
                i += 1
        return 0 < i < 2

    def remove_dead_ends(self, level):
        """Removes some of the dead ends of the maze"""
        done = False
        while not done:
            done = True
            # Check for dead ends
            for tile in self.corridor_tiles:
                if self.is_dead_end(tile, level):
                    tile.set_type(TileTypes.WALL)
                    self.corridor_tiles.remove(tile)
                    # Keep checking
                    done = False

    def generate_doors(self, level_with_corridors):
        # For each room, pick a number of doors
        for room in self.rooms:
            doornum = randint(1, 5)
            while doornum:
                choice(room.doors).set_type(TileTypes.FLOOR)
                doornum -= 1
        return level_with_corridors

    def find_startingtile(self, level_with_rooms):
        starting = False
        while not starting:
            starting = choice(level_with_rooms.tiles)
            # Can't start digging inside the rooms!
            for room in self.rooms:
                overlap = False
                if room.overlap_tile(starting):
                    overlap = True
            if not overlap:
                x, y = starting.coor
                if not (x % 2) or not (y % 2):
                    starting = False
                else:
                    self.logview.post("Startingtile: x: {} y: {}".format(x, y), MsgType.DEBUG)
                    self.startingtile = starting
                    return starting

    def generate_corridors(self, level_with_rooms):
        start = self.find_startingtile(level_with_rooms)
        cells = list()
        cells.append(start)
        while cells:
            current = choice(cells)
            print(current)
            current.set_type(TileTypes.FLOOR)
            self.corridor_tiles.append(current)
            one_step_valid = list()
            two_step_valid = list()
            for key in cons.FOUR_DIRECTIONS:
                tup = cons.FOUR_DIRECTIONS.get(key)
                x, y = current.coor
                neig = level_with_rooms.get_tile_neighbour(x, y, tup, 2)
                # TODO: What if the first tile we looked at was off the map!?
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
            width = self.randint_odd(6, 16)
            height = self.randint_odd(6, 16)
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
