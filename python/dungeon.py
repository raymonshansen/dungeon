"""Dungeon module."""

import pygame as pg
from random import choice

import constants as cons
from map_mod import Map
from typebank import TypeBank
from tiletypes import ActorTypes, get_actorsprites, get_actornames
from dungeon_generator import generate_dungeon
from message import MsgType


TURN_COST = 1000


class Hero():
    def __init__(self, x, y, name, speed, bank):
        self.x = x
        self.y = y
        self.speed = speed
        self.next_action = False
        self.energy = 1000
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

    def get_energy(self):
        self.energy += self.speed

    def do_action(self, action=None):
        # return self.next_action.get_cost()
        self.energy -= 500
        self.next_action = False

    def set_action(self, action):
        self.next_action = action

    def can_take_turn(self):
        return self.energy >= TURN_COST


class Monster():
    def __init__(self, x, y, speed, bank, atype, name):
        self.x = x
        self.y = y
        self.speed = speed
        self.tilebank = bank
        self.type = atype
        self.next_action = True
        self.energy = 0
        self.name = name

    def draw(self, mapsurface):
        coor = (self.x * cons.TILE_D, self.y * cons.TILE_D)
        mapsurface.blit(self.tilebank.get_type(self.type), coor)

    def get_energy(self):
        self.energy += self.speed

    def do_action(self, action=None):
        """Each action will be an instance of a class.
        This way they can be given to anyone for
        easy moding of behaviour.
        """
        # return self.next_action.get_cost()
        self.energy -= 1000
        # Monsters are always ready!
        self.next_action = True

    def set_action(self, action):
        self.next_action = action

    def can_take_turn(self):
        return self.energy >= TURN_COST


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
        self.actor_idx = 0

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
            actors.append(Monster(x, y, 50, bank, typ, get_actornames().get(typ)))

        return actors

    def tick(self):
        # Loop through monsters and player alike.
        # If it now has enough to do an action, we ask it what
        current_actor = self.actors[self.actor_idx]
        if current_actor.can_take_turn():
            # Ask it what it wants to do, all monsters will know
            action = current_actor.next_action
            # If it had an action prepared
            if action:
                current_actor.do_action()
                string = current_actor.name + " " + str(current_actor.energy)
                self.logview.post(string, MsgType.INFO)
                # This will somehow deduct energy from the actor
                # Give the current one some energy based on its speed attribute
                current_actor.get_energy()
                # Move on to the next
                self.actor_idx = (self.actor_idx + 1) % len(self.actors)
            # Only the player will sometimes NOT have decided what to do!
            else:
                # This will wait for the player to give the hero an action
                return
        # If it could not yet take a turn
        else:
            # It gets some energy back
            current_actor.get_energy()
            # Move on to the next
            self.actor_idx = (self.actor_idx + 1) % len(self.actors)

    def handle_player_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.hero.y -= 1
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.hero.y += 1
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.hero.x -= 1
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.hero.x += 1
            # Test time management
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                # Eventually, this will inject the appropriate action instance
                # which governs itself and has it's own cost etc.
                self.hero.set_action(True)

    def update(self, events):
        """Handle turn-based game loop."""
        self.tick()
        self.handle_player_events(events)

    def draw_actors(self, screen):
        """Draw the actorsurface and blit it onto the main screen."""
        for actor in self.actors:
            actor.draw(self.mapsurface)
        screen.blit(self.mapsurface, cons.MAP_POS)

    def draw(self, screen):
        """Draws the map on the screen."""
        # print(str((self.hero.x, self.hero.y)), MsgType.DEBUG)
        self.map.draw(screen, self.hero.x, self.hero.y)
        # Then we draw all the actors!
        self.draw_actors(screen)
