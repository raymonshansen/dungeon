"""Map-module."""

import pygame
from math import sqrt

import constants as cons
from tile import Tile
from tiletypes import translate_dict, TileStatus
from utils import plot_line, plot_circle


class Map():
    """Map class holds the size of the map-view and the entire map.

    Contains various methods for working with the map.
    """

    def __init__(self, surface, pos_rect, bank, mapfile):
        """Construct a map."""
        self.map_view = surface
        self.topleft = pos_rect
        self.dirty = True
        self.view_width = cons.MAP_VIEW_TW
        self.view_height = cons.MAP_VIEW_TH
        self.width = 0
        self.height = 0
        self.tiles = list()
        self.map = self.load_map(mapfile, bank)
        self.set_walltypes()

    def setup_tiles(self, w, h, bank):
        """Fill the map with default tiles."""
        return [Tile(x, y, bank) for y in range(h) for x in range(w)]

    def set_types(self, maplist):
        """Set types given by the maplist."""
        for tile, filtype in zip(self.tiles, maplist):
            tile.set_type(filtype)

    def load_map(self, filename, bank):
        """Load a map from a .txt file."""
        with open(filename, 'rt') as file:
            # Get the width and heigth of the map.
            maplist = list()
            lines = file.readlines()
            self.width, self.height = [int(x) for x in lines[0].split()]
            # Load the rest into a list.
            for line in lines[1:]:
                for x in line.strip():
                    maplist.append(int(x))

            # Setup the tiles
            self.tiles = self.setup_tiles(self.width, self.height, bank)
            # Finally set all tile-types from the maplist
            self.set_types(maplist)

    def get_tile(self, x, y):
        """Take an x and y, returns the tile at that coordinate.

        Return 0 if coordinate is off the map.
        """
        if (0 <= x < self.width) and (0 <= y < self.height):
            # print(f"{x}, {y} - {(y*self.height)+x}")
            return self.tiles[(y * self.height) + x]
        else:
            return 0

    def get_tile_neighbours(self, x, y):
        """Take an x and y.

        returns all tiles around that tile.
        Might contain Nones (see get_tile)
        """
        res = list()
        for key in cons.DIRECTIONS:
            tup = cons.DIRECTIONS.get(key)
            res.append(self.get_tile(x + tup[0], y + tup[1]))
        return res

    def get_tiles_along_line(self, x1, y1, x2, y2):
        """Return all tiles along the line from (x1, y1) and (x2, y2)."""
        coordinates = plot_line(x1, y1, x2, y2)
        ret = [self.get_tile(cor[0], cor[1]) for cor in coordinates]
        return ret

    def get_tiles_around_circle(self, x, y, radius):
        """Return all tiles along circumference of a circle with radius."""
        coordinates = plot_circle(x, y, radius)
        ret = [self.get_tile(cor[0], cor[1]) for cor in coordinates]
        return ret

    def get_wall_list(self):
        """Return a list of all the tiles that should be walls.

        (all tiles that have an adjacent floor-tile)
        """
        wall_to_be = list()
        for tile in self.tiles:
            # If it's not a floor-tile
            if tile.get_type() != 1:
                all_neighbours = self.get_tile_neighbours(tile.x, tile.y)
                neighbours = [x for x in all_neighbours if x != 0]
                for neighb_tile in neighbours:
                    # but one of the adjacent ones are
                    # add to the list, if it wasn't already
                    if neighb_tile.get_type() == 1 and tile not in wall_to_be:
                        wall_to_be.append(tile)
        return wall_to_be

    def set_walltypes(self):
        """Set the wall-type surrounding a floor-tile."""
        walltiles = self.get_wall_list()
        for tile in walltiles:
            neighbours = self.get_tile_neighbours(tile.x, tile.y)
            mask = 0
            for i, n_tile in enumerate(neighbours):
                if n_tile == 0:
                    pass
                elif n_tile.get_type() == 1:
                    mask += 2**i
            tile.set_type(translate_dict.get(mask, 0))

    def refresh_visibility(self, x, y, radius):
        """Refresh the visibility given a certain point."""
        # Paint it black before we start.
        for tile in self.tiles:
            tile.set_light(255)
        # Assume the player isn't blind.
        self.get_tile(x, y).status = TileStatus.EXPLORED
        self.get_tile(x, y).set_light(0)

        for octant_num in range(8):
            self.refresh_octant(x, y, octant_num, radius)

    def refresh_octant(self, x, y, oct_num, radius):
        """Refresh which octant we're in."""
        line = ShadowLine()
        fullshadow = False
        for row_num in range(radius):
            oct_x, oct_y = self.transform_oct(row_num, 0, oct_num)
            ppx = x + oct_x
            ppy = y + oct_y
            # Bail if we go off the map!
            if not self.get_tile(ppx, ppy):
                break
            for col_num in range(row_num + 1):
                oct_x, oct_y = self.transform_oct(row_num, col_num, oct_num)
                px = x + oct_x
                py = y + oct_y

                # Bail if we go off the map!
                if not self.get_tile(px, py):
                    break
                # Safely get the tile to work with
                tile = self.get_tile(px, py)

                if fullshadow:
                    tile.set_light(255)
                else:
                    projection = self.project_tile(row_num, col_num)

                    # Set the visibility of this tile.
                    vis = not line.is_in_shadow(projection)
                    dark = line.is_in_shadow(projection)

                    if dark:
                        visibility = 255
                    else:
                        visibility = 0
                        tile.status = TileStatus.EXPLORED
                    tile.set_light(visibility)

                    # Add any opaque tiles to the shadow map.
                    if vis and tile.is_wall():
                        tile.set_light(0)

                    if not dark and tile.is_wall():
                        line.add(projection)
                        fullshadow = line.is_full_shadow()

    def transform_oct(self, row_num, col_num, octant_num):
        """Switch octant based on a number(octant_num) from 0-7."""
        switcher = {0: (col_num, -row_num),
                    1: (row_num, -col_num),
                    2: (row_num, col_num),
                    3: (col_num, row_num),
                    4: (-col_num, row_num),
                    5: (-row_num, col_num),
                    6: (-row_num, -col_num),
                    7: (-col_num, -row_num)
                    }
        return switcher.get(octant_num)

    def project_tile(self, row_num, col_num):
        """Create a Shadow-object.

        Return Shadow that corresponds to the projected
        silhouette of the tile at row_num, col_num.
        """
        topleft = col_num / (row_num + 2)
        bottomright = (col_num + 1) / (row_num + 1)

        return Shadow(topleft, bottomright)

    def draw(self, screen, playerx, playery):
        """Blit all tiles visible in the map view."""
        if self.dirty:
            self.refresh_visibility(playerx, playery, 10)
            self.map_view.fill(pygame.color.Color("antiquewhite"))

            # Blit tiles in the current view
            leftx = playerx - (self.view_width - 1) // 2
            lefty = playery - (self.view_height - 1) // 2
            for x in range(leftx, leftx + self.view_width):
                for y in range(lefty, lefty + self.view_height):
                    tile = self.get_tile(x, y)
                    # tile == 0 if its off the map
                    if tile:
                        tile.draw(self.map_view, x - leftx, y - lefty)

            red = pygame.color.Color("red")
            screen.blit(self.map_view, self.topleft)

            self.dirty = True

            # Blit fake player pos
            x = (playerx - leftx) * cons.TILE_D + 16
            y = (playery - lefty) * cons.TILE_D + 16
            pygame.draw.circle(screen, red, (x, y), 10, 2)


class Shadow():
    """Represent a Shadow."""

    def __init__(self, start, end):
        """Shadow covers tiles from start to end."""
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Shadow({self.start}, {self.end})"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return self.start <= other.start

    def __add__(self, other):
        return Shadow(min(self.start, other.start), max(self.end, other.end))

    def covers(self, other):
        """Return True if other is completely covered by this one."""
        return self.start <= other.start and self.end >= other.end

    def adjacent(self, other):
        """Return True if other and self are adjacent
        or have any overlapping area."""
        return other.start <= self.end or self.start >= other.end


class ShadowLine():
    """Represent a line of Shadow-objects."""

    def __init__(self, shadows=None):
        """Is basically a list."""
        self.shadows = list()
        incoming = shadows or list()
        for shadow in incoming:
            self.add(shadow)

    def __repr__(self):
        return "ShadowLine([{}])".format(", ".join(repr(x) for x in self.shadows))

    def __eq__(self, other):
        return len(self.shadows) == len(other.shadows) and \
            all(x == y for x, y in zip(self.shadows, other.shadows))

    def is_in_shadow(self, projection):
        """Return true if any shadow in the line covers the tile."""
        return any(shadow.covers(projection) for shadow in self.shadows)

    def contains_overlap(self):
        for x in range(1, len(self.shadows)):
            prev = self.shadows[x - 1]
            curr = self.shadows[x]
            if prev.adjacent(curr):
                return True
        return False

    def coalesce(self):
        while self.contains_overlap():
            new_shadows = list()
            for x, y in zip(self.shadows, self.shadows[1:]):
                if x.adjacent(y):
                    new_shadows.append(x + y)
                else:
                    new_shadows.append(x)
            self.shadows = new_shadows

    def add(self, newshadow):
        """Add a new Shadow to the line,
        coalescing it into a bigger shadow if."""
        self.shadows = sorted(self.shadows + [newshadow])
        self.coalesce()

    def is_full_shadow(self):
        """Return true if whole row is in shadow."""
        length = len(self.shadows)
        start = self.shadows[0].start
        end = self.shadows[0].end
        # print(f"length: {length} - start: {start} - end: {end}")
        return length == 1 and start == 0 and end == 1
