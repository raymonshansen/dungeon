import pygame as pg
from config import colors, TILESIZE
from utils import plot_line
from operator import itemgetter, attrgetter
import random

class Room():
    """Class to hold all info about a room in a dungeon"""
    def __init__(self, tilelist, roomid, layout, color=(255, 255, 255)):
        """Room class constructor"""
        self.layout = layout
        self.tiles = tilelist
        self.id = roomid
        self.color = colors[self.id % len(colors)]
        self.smallestx = sorted(self.tiles, key=attrgetter('pos.x'))[0].pos.x
        self.greatestx = sorted(self.tiles, key=attrgetter('pos.x'), reverse=True)[0].pos.x
        self.smallesty = sorted(self.tiles, key=attrgetter('pos.y'))[0].pos.y
        self.greatesty = sorted(self.tiles, key=attrgetter('pos.y'), reverse=True)[0].pos.y
        self.doornum = random.randint(1, 4)
        self.entry = self.possible_doors()

    def find_edge(self, sorted_tiles, value):
        edge = list()
        point = attrgetter(value)
        edgevalue = point(sorted_tiles[0])
        for tile in sorted_tiles:
            if point(tile) == edgevalue:
                edge.append(tile)
        return edge

    def place_walls(self):
        """Builds walls on all tiles surrounding the room"""

    def possible_doors(self):
        """Set random number of doors"""
        n = self.find_edge(sorted(self.tiles, key=attrgetter('pos.y')), 'pos.y')
        s = self.find_edge(sorted(self.tiles, key=attrgetter('pos.y'), reverse=True), 'pos.y')
        e = self.find_edge(sorted(self.tiles, key=attrgetter('pos.x')), 'pos.x')
        w = self.find_edge(sorted(self.tiles, key=attrgetter('pos.x'), reverse=True), 'pos.x')
        doors = n + s + e + w
        return doors

    @property
    def area(self):
        return len(self.tiles)

    def draw_nodes(self, screen):
        """Draw each node N of the polygon that makes up the room"""
        for tile in self.tiles:
            tile.draw_tile(screen)
