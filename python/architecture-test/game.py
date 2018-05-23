import pygame as pg

import constants as cons
from dungeon import Dungeon
from logview import LogView
from message import MsgType
from statsview import StatView


TURN_COST = 1000


class Hero():
    def __init__(self, name):
        self.speed = 100
        self.next_action = False
        self.energy = 0
        self.name = name

    def do_action(self, action=None):
        # return self.next_action.get_cost()
        self.energy -= 500
        self.next_action = False

    def set_action(self, action):
        self.next_action = action

    def can_take_turn(self):
        return self.energy >= TURN_COST


class Monster():
    def __init__(self, name):
        self.speed = 50
        self.next_action = False
        self.energy = 0
        self.name = name

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

class Game():
    def __init__(self, screen, statemanager):
        pg.init()
        self.screen = screen
        self.statemanager = statemanager
        self.setup()

    def setup(self):
        logsurface = pg.Surface(cons.LOG_DIM)
        self.logview = LogView(logsurface, cons.LOG_POS)
        dungeonsurf = pg.Surface(cons.MAP_DIM)
        self.dungeon = Dungeon(dungeonsurf, self.logview)
        statsurface = pg.Surface(cons.STAT_DIM)
        self.statview = StatView(statsurface, cons.STAT_POS)

        self.px = 16
        self.py = 16

        # Testing time-management
        self.hero = Hero("Hero")
        self.rat = Monster("Rat")
        self.actors = [self.hero, self.rat]

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            # Quit the game.
            if event.type == pg.QUIT:
                self.statemanager.switch_state('EXITING')
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.statemanager.switch_state('EXITING')
                break
            # Move the "player".
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.py -= 1
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.py += 1
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.px -= 1
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.px += 1
            # Test log
            if event.type == pg.KEYDOWN and event.key == pg.K_l:
                self.logview.post("Testing log.", MsgType.BATTLE)
            if event.type == pg.KEYDOWN and event.key == pg.K_n:
                string = "Testing log with way too much text so that it will need to wrap many, many times to fit into the text-view."
                self.logview.post(string, MsgType.INFO)
            if event.type == pg.KEYDOWN and event.key == pg.K_i:
                self.logview.post("DEBUG TEXT.", MsgType.DEBUG)
            # Test StateManager
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.statemanager.switch_state('MAINMENU')
            # Reload level
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.setup()
            # Test time management
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                # Eventually, this will inject the appropriate action instance
                # which governs itself and has it's own cost etc.
                self.hero.set_action(True)

    def tick(self):
        # If the player doesn't go no one else does either
        if self.hero.can_take_turn() and self.hero.next_action:
            for actor in self.actors:
                # Give everyone some energy
                # This amount will be a function of actors speed later.
                # For now, let's see if it works at all.
                actor.energy += 20
                # Everyone who can, gets to go!
                if actor.can_take_turn():
                    # Some actions spend less of your 1000 energy.
                    # You will then regain a turn faster.
                    actor.do_action()
                    self.logview.post(actor.name + " " + str(actor.energy), MsgType.INFO)
        elif not self.hero.can_take_turn():
            for actor in self.actors:
                actor.energy += 20
        else:
            return

# Run from the while loop of state-manager:
    def update(self):
        self.handle_events()
        self.tick()

    def draw(self):
        self.dungeon.draw(self.screen, self.px, self.py)
        self.statview.draw(self.screen)
        self.logview.draw(self.screen)
