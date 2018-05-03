import pygame as pg
import sys

from game import Game
from mainmenu import MainMenu
import constants as cons


class StateManager():
    def __init__(self):
        self.window_w = cons.TILE_D*cons.SCREEN_TW
        self.window_h = cons.TILE_D*cons.SCREEN_TH
        self.screensize = (self.window_w, self.window_h)
        self.screen = pg.display.set_mode(self.screensize)
        self.game_state = Game(self.screen, self)
        self.main_menu_state = MainMenu(self.screen, self)
        self.current_state = self.game_state
        self.done = False

    def switch_state(self, state):
        if state == 'MAINMENU':
            self.current_state = self.main_menu_state
        elif state == 'GAME':
            self.current_state = self.game_state
        elif state == 'EXITING':
            self.done = True

    def exit(self):
        print("Exiting nicely...")
        pg.quit()
        sys.exit()

    def loop(self):
        while not self.done:
            self.current_state.update()
            self.current_state.draw()
            pg.display.update()
        
        self.exit()


if __name__ == '__main__':
    program = StateManager()
    program.loop()
