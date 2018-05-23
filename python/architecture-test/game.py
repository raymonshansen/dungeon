import pygame as pg

import constants as cons
from dungeon import Dungeon
from logview import LogView
from message import MsgType


class StatView():
    def __init__(self, surface, pos_rect):
        self.surface = surface
        self.topleft = pos_rect
        self.dirty = True

    def draw(self, screen):
        if self.dirty:
            self.surface.fill(pg.color.Color("black"))
            screen.blit(self.surface, self.topleft)


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
            # Move the player.
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.py -= 1
                string = "{}, {}".format(self.px, self.py)
                #self.logview.post(string, MsgType.INFO)
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.py += 1
                string = "{}, {}".format(self.px, self.py)
                #self.logview.post(string, MsgType.INFO)
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.px -= 1
                string = "{}, {}".format(self.px, self.py)
                #self.logview.post(string, MsgType.INFO)
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.px += 1
                string = "{}, {}".format(self.px, self.py)
                # self.logview.post(string, MsgType.INFO)
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

# Run from the while loop of state-manager:
    def update(self):
        self.handle_events()

    def draw(self):
        self.dungeon.draw(self.screen, self.px, self.py)
        self.statview.draw(self.screen)
        self.logview.draw(self.screen)
