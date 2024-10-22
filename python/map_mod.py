"""Map-module."""

import pygame
from random import randint

import constants as cons
from tile import Tile
from tiletypes import TileStatus, TileTypes
from typebank import TypeBank
from utils import plot_line
from tiletypes import get_tilenames


class Map():
    """Map class holds the size of the map-view and the entire map.

    Contains various methods for working with the map.
    """

    def __init__(self, surface, logview, width, height):
        """Construct a map."""
        self.map_view = surface
        self.logview = logview
        self.width = width
        self.height = height
        self.topleft = cons.MAP_POS
        self.dirty = True
        self.view_width = cons.MAP_VIEW_TW
        self.view_height = cons.MAP_VIEW_TH
        self.tiles = self.setup_tiles(self.width, self.height, TypeBank(get_tilenames))
    
    def get_width_height(self):
        """Return the width and height of the map."""
        return self.width, self.height

    def set_type(self, x, y, tiletype):
        """Enables setting a tile type from outside the map."""
        if self.width <= x < 0:
            return
        if self.height <= y < 0:
            return
        self.get_tile(x, y).set_type(tiletype)

    def get_type(self, x, y):
        """Return the tile-type at the given coordinate."""
        if self.width <= x < 0:
            return
        if self.height <= y < 0:
            return
        return self.get_tile(x, y).get_type()

    def setup_tiles(self, w, h, bank):
        """Fill the map with floor tiles."""
        tiles = [Tile(x, y, bank) for y in range(h) for x in range(w)]
        for tile in tiles:
            # Test randomness...
            if randint(0, 2):
                tile.set_type(TileTypes.WALL)
            else:
                tile.set_type(TileTypes.WALL)
        return tiles

    def get_tile(self, x, y):
        """Take an x and y, returns the tile at that coordinate.
        Return 0 if coordinate is off the map.
        """
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.tiles[(y * self.height) + x]
        else:
            return 0

    def get_tile_neighbour(self, tile, dir_tup, numstep=1):
        """Return the neighbour-tile
        numstep in that dierction. Might contain zeroes (see get_tile).
        """
        x, y = tile.coor
        xstep = dir_tup[0] * numstep
        ystep = dir_tup[1] * numstep
        return self.get_tile(x + xstep, y + ystep)

    def get_tile_neighbours(self, x, y):
        """Take an x and y, returns all tiles around that tile.
        Might contain zeroes (see get_tile).
        """
        res = list()
        for key in cons.DIRECTIONS:
            tup = cons.DIRECTIONS.get(key)
            res.append(self.get_tile_neighbour(x, y, tup))
        return res

    def get_tiles_along_line(self, x1, y1, x2, y2):
        """Return all tiles along the line from (x1, y1) and (x2, y2)."""
        coordinates = plot_line(x1, y1, x2, y2)
        ret = [self.get_tile(cor[0], cor[1]) for cor in coordinates]
        return ret
    
    def get_tiles_in_rect(self, left, top, width, height):
        """Return a list of all the tiles in the rectangle made
        by left, top, width and height.
        Might contain zeroes if part of rectangle is outside map.
        """
        retlist = list()
        for x in range(left, left + width):
            for y in range(top, top + height):
                retlist.append(self.get_tile(x, y))
        return retlist

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
                        visibility = (230/radius) * row_num
                        tile.status = TileStatus.EXPLORED
                    tile.set_light(visibility)

                    # Add any opaque tiles to the shadow map.
                    if vis and tile.is_wall:
                        tile.set_light(visibility)

                    if not dark and tile.is_wall:
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
            self.refresh_visibility(playerx, playery, 5)
            self.map_view.fill(pygame.color.Color("black"))

            # Blit tiles in the current view
            leftx = playerx - (self.view_width - 1) // 2
            lefty = playery - (self.view_height - 1) // 2
            for x in range(leftx, leftx + self.view_width):
                for y in range(lefty, lefty + self.view_height):
                    tile = self.get_tile(x, y)
                    # tile == 0 if its off the map
                    if tile:
                        tile.draw(self.map_view, x - leftx, y - lefty)

            screen.blit(self.map_view, self.topleft)

            self.dirty = True
            # Blit fake player pos
            red = pygame.color.Color("red")
            x = (playerx - leftx) * cons.TILE_D + (cons.TILE_D//2)
            y = (playery - lefty) * cons.TILE_D + (cons.TILE_D//2)
            pygame.draw.circle(screen, red, (x, y), (cons.TILE_D//4), 2)


class Shadow():
    """Represent a Shadow."""

    def __init__(self, start, end):
        """Shadow covers tiles from start to end."""
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Shadow({}, {})'.format(self.start, self.end)

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
        return length == 1 and start == 0 and end == 1
