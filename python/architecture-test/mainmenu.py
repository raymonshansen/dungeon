import os
import pygame as pg
import constants as cons


class MainMenuItem():
    def __init__(self, pos, surface, text, bgcolor):
        self.pos = pos
        self.fontpath = os.path.join('Avara.otf')
        self.font = pg.font.Font(self.fontpath, cons.MAINMENU_FONTSIZE)
        self.text = text
        self.default_col = pg.color.Color("antiquewhite")
        self.selected_col = pg.color.Color("red")
        self.bgcolor = bgcolor
        self.textsurf = self.get_text_surface()
        self.selected = False

    def set_selected(self):
        self.selected = True

    def set_deselected(self):
        self.selected = False

    def get_text_surface(self):
        return self.font.render(self.text, True, self.default_col, self.bgcolor)

    def set_text_color(self, color):
        self.textsurf = self.font.render(self.text, True, color, self.bgcolor)

    def draw(self, surface):
        if self.selected:
            self.set_text_color(self.selected_col)
        elif not self.selected:
            self.set_text_color(self.default_col)
        surface.blit(self.textsurf, self.pos)


class MainMenu():
    def __init__(self, screen, statemanager):
        self.statemanager = statemanager
        self.screen = screen
        self.bgcolor = pg.color.Color("black")
        self.menu_items = self.item_list()
        self.current_choice = 0
        self.menu_items[self.current_choice].set_selected()

    def item_list(self):
        retlist = list()
        menuitemnames = ["Resume", "Quit"]
        for idx, item in enumerate(menuitemnames):
            dist_from_top = (idx * 100) + 200
            pos = (cons.SCREEN_W_PX//2, dist_from_top)
            it = MainMenuItem(pos, self.screen, item, self.bgcolor)
            retlist.append(it)
        return retlist

    def up(self):
        self.menu_items[self.current_choice].set_deselected()
        self.current_choice -= 1
        self.current_choice %= len(self.menu_items)        
        self.menu_items[self.current_choice].set_selected()

    def down(self):
        self.menu_items[self.current_choice].set_deselected()
        self.current_choice += 1
        self.current_choice %= len(self.menu_items)
        self.menu_items[self.current_choice].set_selected()

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
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.down()
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.up()

    def update(self):
        self.handle_events()

    def draw(self):
        self.screen.fill(self.bgcolor)
        for menu_item in self.menu_items:
            menu_item.draw(self.screen)
