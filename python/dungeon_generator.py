"""Dungeon generator."""

from random import randint, choice, sample
from time import time

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
        """Return a list of all tiles along the top wall, except corners."""
        x1, y1 = self.left + 1, self.top
        x2, y2 = self.left + self.width - 2, y1
        return self.level.get_tiles_along_line(x1, y1, x2, y2)

    def get_bottom_wall(self):
        """Return a list of all tiles along the bottom wall, except corners."""
        x1, y1 = self.left + 1, self.top + self.height - 1
        x2, y2 = self.left + self.width - 1, y1
        return self.level.get_tiles_along_line(x1, y1, x2, y2)

    def get_left_wall(self):
        """Return a list of all tiles along the left wall, except corners."""
        x1, y1 = self.left, self.top + 1
        x2, y2 = x1, self.top + self.height - 2
        return self.level.get_tiles_along_line(x1, y1, x2, y2)

    def get_right_wall(self):
        """Return a list of all tiles along the right wall, except corners."""
        x1, y1 = self.left + self.width - 1, self.top + 1
        x2, y2 = x1, self.top + self.height - 2
        return self.level.get_tiles_along_line(x1, y1, x2, y2)

    def get_corner_wall(self):
        """Return a list of the four corner-tiles of a room."""
        wallist = list()
        corners = [(self.left, self.top),
                   (self.left, self.top + self.height - 1),
                   (self.left + self.width - 1, self.top),
                   (self.left + self.width - 1, self.top + self.height - 1)]
        for corner in corners:
            wallist.append(self.level.get_tile(*corner))
        return wallist

    def random_tile_from_list(self, tiles, tilenum):
        """Return a random tile from a list of tiles."""
        return sample(tiles, tilenum)

    def wall_tiles(self):
        """Return the list of all the walltiles of a room."""
        wallist = list()
        wallist += self.get_top_wall()
        wallist += self.get_bottom_wall()
        wallist += self.get_left_wall()
        wallist += self.get_right_wall()
        wallist += self.get_corner_wall()
        return wallist

    def set_doors(self, doornum):
        """Set a random number of doors. Same tile might be chosen as
        door several times."""
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
            door = choice(possible_doors)
            self.doors.append(door)
            doornum -= 1
        # Finally dig those doors!
        for door in self.doors:
            door.set_type(TileTypes.FLOOR)

    def floor_tiles(self):
        """Find the floor tiles of a room."""
        floorlist = list()
        for x in range(self.left + 1, self.left + self.width - 1):
            for y in range(self.top + 1, self.top + self.height - 1):
                floorlist.append(self.level.get_tile(x, y))
        return floorlist

    def set_floor_tiles(self):
        """Set all the floor-tiles in a room."""
        for tile in self.floor:
            tile.set_type(TileTypes.FLOOR)

    @property
    def floor_area(self):
        return (self.width - 2) * (self.height - 2)

    @property
    def total_area(self):
        return (self.width) * (self.height)


"""Generates the dungeon with the help of the rooms."""


def generate_dungeon(dungeon):
    """Wrapper for various stages of random generation."""
    start = time()
    generate_rooms(dungeon)
    delta = time() - start
    string = "generate_rooms( ) " + "{}".format(delta) + " sec"
    dungeon.logview.post(string, MsgType.DEBUG)

    start = time()
    generate_corridors(dungeon)
    delta = time()-start
    string = "generate_corridors( ) " + "{}".format(delta) + " sec"
    dungeon.logview.post(string, MsgType.DEBUG)

    start = time()
    generate_doors(dungeon)
    delta = time()-start
    string = "generate_doors( ) " + "{}".format(delta) + " sec"
    dungeon.logview.post(string, MsgType.DEBUG)

    start = time()
    remove_dead_ends(dungeon)
    delta = time()-start
    string = "remove_dead_ends( ) " + "{}".format(delta) + " sec"
    dungeon.logview.post(string, MsgType.DEBUG)


def is_dead_end(dungeon, tile):
    """Return true if tile is a dead end."""
    i = 0
    for _, tup in cons.FOUR_DIRECTIONS.items():
        neighbour = dungeon.map.get_tile_neighbour(tile, tup)
        if neighbour.get_type() == TileTypes.FLOOR:
            i += 1
    return 0 < i < 2


def remove_dead_ends(dungeon):
    """Remove all of the dead ends of the maze."""
    done = False
    while not done:
        done = True
        # Check for dead ends
        for tile in dungeon.corridor_tiles:
            if is_dead_end(dungeon, tile):
                tile.set_type(TileTypes.WALL)
                dungeon.corridor_tiles.remove(tile)
                done = False


def generate_doors(self):
    """Add doors to some of the walls that lead to corridor-tiles."""
    # For each room, pick a number of doors
    for room in self.rooms:
        doornum = randint(1, 5)
        room.set_doors(doornum)


def find_maze_start(dungeon):
    """Find a valid place for the maze-algorithm to start."""
    starting = False
    map_width, map_height = dungeon.map.get_width_height()
    while not starting:
        x = choice([i for i in range(1, map_width, 2)])
        y = choice([i for i in range(1, map_height, 2)])
        starting = dungeon.map.get_tile(x, y)
        # Can't start digging inside the rooms!
        overlap = False
        for room in dungeon.rooms:
            if room.overlap_tile(starting):
                overlap = True
                break
        if not overlap:
            return starting
        else:
            # Keep looking!
            starting = False


def generate_corridors(dungeon):
    """Maze algorithm that digs a perfect maze(no loops)."""
    start = find_maze_start(dungeon)
    cells = list()
    cells.append(start)
    while cells:
        current = choice(cells)
        current.set_type(TileTypes.FLOOR)
        dungeon.corridor_tiles.append(current)
        can_dig = list()
        valid_neighbours = list()
        # Get all valid neighbours and the tiles to dig in between
        for key in cons.FOUR_DIRECTIONS:
            tup = cons.FOUR_DIRECTIONS.get(key)
            neig = dungeon.map.get_tile_neighbour(current, tup, 2)
            dig = dungeon.map.get_tile_neighbour(current, tup)
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
            dungeon.corridor_tiles.append(can_dig[idx])
            cells.append(valid_neighbours[idx])


def generate_rooms(dungeon):
    """Try to place rooms of various size within the current level space.
    Increase the number of maxtries to have higher room density.
    """
    roomnum = randint(7, 14)
    maxtries = 10
    tries = 0
    actual_rooms = 0
    dungeon.logview.post("Roomnum: {}".format(roomnum), MsgType.INFO)
    dungeon.logview.post("Maxtries: {}".format(maxtries), MsgType.INFO)
    map_w, map_h = dungeon.map.get_width_height()
    width_range = [i for i in range(7, 11, 2)]
    height_range = [i for i in range(7, 11, 2)]

    while tries < maxtries and len(dungeon.rooms) < roomnum:
        width = choice(width_range)
        height = choice(height_range)
        left = choice([i for i in range(2, map_w - width, 2)])
        top = choice([i for i in range(2, map_h - height, 2)])
        tiles_in_rom = dungeon.map.get_tiles_in_rect(left, top, width, height)
        # Make sure we don't overlap existing rooms
        good = True
        for existing_room in dungeon.rooms:
            for tile in tiles_in_rom:
                if existing_room.overlap_tile(tile):
                    good = False
        if good:
            room = Room(left, top, width, height, dungeon.map)
            dungeon.rooms.append(room)
            actual_rooms += 1
        tries += 1
    dungeon.logview.post("Actual rooms: {}".format(actual_rooms), MsgType.INFO)
