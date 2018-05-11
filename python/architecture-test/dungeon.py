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
        self.set_floor_tiles()
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
        wallist += self.get_top_wall()
        wallist += self.get_bottom_wall()
        wallist += self.get_left_wall()
        wallist += self.get_right_wall()
        wallist += self.get_corner_wall()
        return wallist

    def set_doors(self, doornum):
        possible_doors = list()
        list_and_dir = [(self.get_top_wall(), 'N'),
                        (self.get_bottom_wall(), 'S'),
                        (self.get_left_wall(), 'W'),
                        (self.get_right_wall(), 'E')]
        for tiles, dirr in list_and_dir:
            for tile in tiles:
                direction = cons.FOUR_DIRECTIONS.get(dirr)
                neighbour = self.level.get_tile_neighbour(tile, direction)
                # A door has to lead somewhere!
                if neighbour and neighbour.get_type() == TileTypes.FLOOR:
                    possible_doors.append(tile)
        while doornum:
            self.doors.append(choice(possible_doors))
            doornum -= 1
        # Finally dig those doors!
        for door in self.doors:
            door.set_type(TileTypes.FLOOR)

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
        self.map = Map(self.screen, self.logview, 33, 33)
        self.generate_dungeon()

    def generate_dungeon(self):
        """Wrapper for various stages of random generation."""
        self.generate_rooms()
        self.generate_corridors()
        self.generate_doors()
        self.remove_dead_ends()

    def is_dead_end(self, tile):
        """Return true if tile is a dead end."""
        i = 0
        for _, tup in cons.FOUR_DIRECTIONS.items():
            neighbour = self.map.get_tile_neighbour(tile, tup)
            if neighbour.get_type() == TileTypes.FLOOR:
                i += 1
        return 0 < i < 2

    def remove_dead_ends(self):
        """Remove all of the dead ends of the maze."""
        done = False
        while not done:
            done = True
            # Check for dead ends
            for tile in self.corridor_tiles:
                if self.is_dead_end(tile):
                    tile.set_type(TileTypes.WALL)
                    self.corridor_tiles.remove(tile)
                    done = False

    def generate_doors(self):
        # For each room, pick a number of doors
        for room in self.rooms:
            doornum = randint(1, 5)
            room.set_doors(doornum)

    def find_maze_start(self):
        starting = False
        map_width, map_height = self.map.get_width_height()
        while not starting:
            x = choice([i for i in range(1, map_width, 2)])
            y = choice([i for i in range(1, map_height, 2)])
            starting = self.map.get_tile(x, y)
            # Can't start digging inside the rooms!
            overlap = False
            for room in self.rooms:
                if room.overlap_tile(starting):
                    overlap = True
                    break
            if not overlap:
                return starting
            else:
                # Keep looking!
                starting = False

    def generate_corridors(self):
        start = self.find_maze_start()
        cells = list()
        cells.append(start)
        while cells:
            current = choice(cells)
            current.set_type(TileTypes.FLOOR)
            self.corridor_tiles.append(current)
            can_dig = list()
            valid_neighbours = list()
            # Get all valid neighbours and the tiles to dig in between
            for key in cons.FOUR_DIRECTIONS:
                tup = cons.FOUR_DIRECTIONS.get(key)
                neig = self.map.get_tile_neighbour(current, tup, 2)
                dig = self.map.get_tile_neighbour(current, tup)
                if neig and dig:
                    neig_is_wall = neig.get_type() == TileTypes.WALL
                    dig_is_wall = dig.get_type() == TileTypes.WALL
                    if neig_is_wall and dig_is_wall:
                        valid_neighbours.append(neig)
                        can_dig.append(dig)

            # Either we don't have any valid directions to go.
            if not valid_neighbours:
                # In which case we go back and pick one of the others.
                cells.remove(current)
            # Or we do.
            else:
                # In which case we pick a random direction to go.
                # This choice can greatly influence the look of the maze!
                # Currently, it's a completely random choice, but it go favor
                # the direction it came from, vertical or horizontal etc.
                idx = randint(0, len(valid_neighbours) - 1)
                valid_neighbours[idx].set_type(TileTypes.FLOOR)
                can_dig[idx].set_type(TileTypes.FLOOR)
                self.corridor_tiles.append(can_dig[idx])
                cells.append(valid_neighbours[idx])

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
        roomnum = randint(7, 17)
        maxtries = 100
        tries = 0
        self.logview.post("Roomnum: {}".format(roomnum), MsgType.INFO)
        self.logview.post("Maxtries: {}".format(maxtries), MsgType.INFO)
        map_w, map_h = self.map.get_width_height()
        while tries < maxtries and len(self.rooms) < roomnum:
            width = self.randint_odd(6, 16)
            height = self.randint_odd(6, 16)
            left = self.randint_even(2, map_w - width)
            top = self.randint_even(2, map_h - height)
            tiles_in_rom = self.map.get_tiles_in_rect(left, top, width, height)
            # Make sure we don't overlap existing rooms
            good = True
            for existing_room in self.rooms:
                for tile in tiles_in_rom:
                    if existing_room.overlap_tile(tile):
                        good = False
            if good:
                room = Room(left, top, width, height, self.map)
                self.rooms.append(room)
            tries += 1

    def draw(self, screen, x, y):
        """Draws the map on the screen."""
        self.map.draw(screen, x, y)
