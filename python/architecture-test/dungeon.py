"""Dungeon module."""

import pygame as pg
from random import choice

import constants as cons
from map_mod import Map
from dungeon_generator import generate_dungeon


class Hero():
    def __init__(self, x, y, name, speed):
        self.x = x
        self.y = y
        self.name = name
        self.speed = speed


class Monster():
    def __init__(self, x, y, name, speed):
        self.x = x
        self.y = y
        self.name = name
        self.speed = speed


class Dungeon():
    """Dungeon class."""

    def __init__(self, surface, logview):
        """Contsructs a random map, items and monsters."""
        self.logview = logview
        self.mapsurface = surface
        self.actorsurface = pg.Surface(cons.MAP_DIM)
        self.corridor_tiles = list()
        self.rooms = list()
        self.map = Map(self.mapsurface, self.logview, 33, 33)
        generate_dungeon(self)
        # Make the hero!
        self.hero = Hero(*choice(self.corridor_tiles).coor, "Hero", 200)
        # Make some monsters!
        self.actors = self.populate()

    def populate(self):
        actors = list()
        # Som random monster types/names
        names = ["Rat", "Goblin", "Bat"]
        # Hero goes in the list with the rest of them.
        actors.append(self.hero)
        # Each room gets a monster
        # Make this depend on some stat of the dungeon later...
        for room in self.rooms:
            actors.append(Monster(*choice(room.floor).coor, choice(names), 50))
        return actors

    def draw(self, screen):
        """Draws the map on the screen."""
        self.map.draw(screen, self.hero.x, self.hero.y)
