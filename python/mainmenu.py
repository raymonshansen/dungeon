import os
import pygame as pg
import constants as cons
from message import Message, MsgType


class MainMenuItem():
    def __init__(self, pos, surface, text):
        self.pos = pos
        self.text = text
        self.fontpath = os.path.join('Avara.otf')
        self.font = pg.font.Font(self.fontpath, cons.MAINMENU_FONTSIZE)
        self.default_col = cons.MAINMENU_DEFAULT_COL
        self.selected_col = cons.MAINMENU_SELECTED_COL
        self.bgcolor = cons.MAINMENU_BGCOL
        self.textsurf = self.get_text_surface()
        self.selected = False

    def get_bottom_left(self):
        return (self.pos[0], self.pos[1]+cons.MAINMENU_FONTSIZE)

    def get_width(self):
        return self.textsurf.get_width()

    def is_selected(self):
        return self.selected

    def set_selected(self):
        self.selected = True

    def set_deselected(self):
        self.selected = False

    def get_text_surface(self):
        return self.font.render(self.text, True, self.default_col, self.bgcolor)

    def get_text(self):
        return self.text

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
        self.func_name = {"Resume": self.resume, "Editor": self.editor, "Quit": self.quit}
        self.bgcolor = cons.MAINMENU_BGCOL
        self.menu_items = self.item_list()
        self.current_choice = 0
        self.menu_items[self.current_choice].set_selected()
        self.infoboxlist = self.infobox_list()
        self.headline = self.get_headline()

    def get_headline(self):
        headline = Message("Dungeon", MsgType.INFO)
        headline.set_size(cons.TILE_D * 4)
        headline.set_rect(cons.SCREEN_W_PX//12, cons.TILE_D, 400, cons.TILE_D * 2)
        headline.set_color(cons.MAINMENU_DEFAULT_COL)
        return headline

    def infobox_list(self):
        retlist = list()
        for text in cons.MAINMENU_ITEM_INFO:
            info = Message(text, MsgType.INFO)
            info.set_size(cons.TILE_D)
            info.set_rect((cons.SCREEN_W_PX//2)+150, cons.TILE_D * 10, cons.SCREEN_W_PX//4, cons.SCREEN_H_PX//2)
            info.set_color(cons.MAINMENU_SELECTED_COL)
            retlist.append(info)
        return retlist

    def item_list(self):
        retlist = list()
        for idx, item in enumerate(cons.MAINMENU_ITEM_LABELS):
            dist_from_top = (idx * cons.TILE_D * 3) + cons.TILE_D * 10
            pos = (cons.SCREEN_W_PX//2-200, dist_from_top)
            it = MainMenuItem(pos, self.screen, item)
            retlist.append(it)
        return retlist

    def up_or_down(self, step):
        """Select next or previous item in the item_list.
        Negative step is down, positive step is up."""
        self.menu_items[self.current_choice].set_deselected()
        self.current_choice -= step
        self.current_choice %= len(self.menu_items)
        self.menu_items[self.current_choice].set_selected()

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            # Quit the game.
            if event.type == pg.QUIT:
                self.statemanager.switch_state('EXITING')
                break
            # Select menu-item
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.up_or_down(-1)
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.up_or_down(1)
            # Call apropriate method from menuitem
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.func_name.get(self.menu_items[self.current_choice].get_text())()

    def resume(self):
        self.statemanager.switch_state('GAME')

    def quit(self):
        self.statemanager.switch_state('EXITING')

    def editor(self):
        print("Editor is forthcoming...")

    def update(self):
        self.handle_events()

    def draw_lines(self, item_info):
        """Draw some ey-candy."""
        # Draw underscore
        item, infobox = item_info
        col = cons.MAINMENU_SELECTED_COL
        x1, y1 = item.get_bottom_left()
        x2, y2 = infobox.get_rect().left-cons.TILE_D//2, y1
        pg.draw.line(self.screen, col, (x1, y1), (x2, y2), 1)
        pg.draw.line(self.screen, col, (x1 + 7, y1 + 7), (x2 - 7, y2 + 7), 1)
        # Draw vertical
        x1, y1 = infobox.get_rect().x-cons.TILE_D//2, infobox.get_rect().y
        pg.draw.line(self.screen, col, (x1, y1), (x2, y2), 1)
        pg.draw.line(self.screen, col, (x1 - 7, y1 + 7), (x2 - 7, y2 + 7), 1)
        # Headline... lines
        hrec = self.headline.get_rect()
        x1, y1 = hrec.left, hrec.bottom + 5
        x2, y2 = hrec.right + hrec.width + hrec.width, hrec.bottom + 5
        pg.draw.line(self.screen, col, (x1, y1), (x2, y2), 1)
        pg.draw.line(self.screen, col, (x1 + 7, y1 + 7), (x2 + 7, y2 + 7), 1)

    def draw(self):
        self.screen.fill(self.bgcolor)
        for item_info in zip(self.menu_items, self.infoboxlist):
            # Draw text first
            item_info[0].draw(self.screen)
            if item_info[0].is_selected():
                item_info[1].draw(self.screen)
                # Then the lines...
                self.draw_lines(item_info)
        self.headline.draw(self.screen)