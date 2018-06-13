import pygame as pg

import constants as cons
from dungeon import Dungeon
from logview import LogView
from message import MsgType
from statsview import StatView


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

    def handle_events(self, events):
        for event in events:
            # Quit the game.
            if event.type == pg.QUIT:
                self.statemanager.switch_state('EXITING')
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.statemanager.switch_state('EXITING')
                break
            # Main menu
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.statemanager.switch_state('MAINMENU')
            # Reload level
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.setup()

    def update(self):
        events = pg.event.get()
        self.handle_events(events)
        self.dungeon.update(events)

    def draw(self):
        self.dungeon.draw(self.screen)
        self.statview.draw(self.screen)
        self.logview.draw(self.screen)
