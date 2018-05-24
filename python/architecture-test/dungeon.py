"""Dungeon module."""

import pygame as pg
from random import choice

import constants as cons
from map_mod import Map
from typebank import TypeBank
from tiletypes import ActorTypes, get_actorsprites
from dungeon_generator import generate_dungeon
from message import MsgType


class Hero():
    def __init__(self, x, y, name, speed, bank):
        self.x = x
        self.y = y
        self.name = name
        self.speed = speed
        self.tilebank = bank
        self.type = ActorTypes.HERO

    def draw(self, mapsurface):
        #coor = (self.x * cons.TILE_D, self.y * cons.TILE_D)
        leftx = self.x - (cons.MAP_VIEW_TW - 1) // 2
        lefty = self.y - (cons.MAP_VIEW_TH - 1) // 2
        x = (self.x - leftx) * cons.TILE_D
        y = (self.y - lefty) * cons.TILE_D
        mapsurface.blit(self.tilebank.get_type(self.type), (x, y))

class Monster():
    def __init__(self, x, y, speed, bank, atype):
        self.x = x
        self.y = y
        self.speed = speed
        self.tilebank = bank
        self.type = atype

    def draw(self, mapsurface):
        coor = (self.x * cons.TILE_D, self.y * cons.TILE_D)
        mapsurface.blit(self.tilebank.get_type(self.type), coor)


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
        x, y = choice(self.corridor_tiles).coor
        self.hero = Hero(x, y, "Hero", 200, TypeBank(get_actorsprites))
        self.logview.post(str((x, y)), MsgType.DEBUG)
        # Make some monsters!
        self.actors = self.populate()

    def populate(self):
        actors = list()
        # Hero goes in the list with the rest of them.
        actors.append(self.hero)
        # Each room gets a monster
        # Make this depend on some stat of the dungeon later...
        for room in self.rooms:
            x, y = choice(room.floor).coor
            bank = TypeBank(get_actorsprites)
            typ = choice(list(ActorTypes)[1::])
            actors.append(Monster(x, y, 50, bank, typ))
        self.logview.post(str(actors), MsgType.DEBUG)
        return actors

    def draw_actors(self, screen):
        """Draw the actorsurface and blit it onto the main screen."""
        for actor in self.actors:
            actor.draw(self.mapsurface)
        screen.blit(self.mapsurface, cons.MAP_POS)

    def draw(self, screen):
        """Draws the map on the screen."""
        #print(str((self.hero.x, self.hero.y)), MsgType.DEBUG)
        self.map.draw(screen, self.hero.x, self.hero.y)
        # Then we draw all the actors!
        self.draw_actors(screen)
