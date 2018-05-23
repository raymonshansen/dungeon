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
        self.next_action = True
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
        self.actor_idx = 0
        self.actors = [Hero("Hero"), Monster("Rat"), Monster("Bat")]

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
                current_actor.energy += 20
                # Move on to the next
                self.actor_idx = (self.actor_idx + 1) % len(self.actors)
            # Only the player will sometimes NOT have decided what to do!
            else:
                # This will wait for the player to give the hero an action
                return
        # If it could not yet take a turn
        else:
            # It gets some energy back
            current_actor.energy += 20
            # Move on to the next
            self.actor_idx = (self.actor_idx + 1) % len(self.actors)

# Run from the while loop of state-manager:
    def update(self):
        self.handle_events()
        self.tick()

    def draw(self):
        self.dungeon.draw(self.screen, self.px, self.py)
        self.statview.draw(self.screen)
        self.logview.draw(self.screen)
