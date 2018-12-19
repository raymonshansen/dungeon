import pygame as pg
import constants as cons
from message import Message, MsgType


class MainMenuItem():
    def __init__(self, idx, surface, label_obj, info_obj):
        self.text_obj = self.calc_label_obj(idx, label_obj)
        self.info_obj = self.calc_info_box(info_obj)
        self.selected = False

    def calc_label_obj(self, idx, label_obj):
        y = (idx * cons.TILE_D * 3) + cons.TILE_D * 10
        x = cons.SCREEN_W_PX // 2 - 200
        w = cons.SCREEN_W_PX // 4
        h = cons.SCREEN_H_PX // 8
        label_obj.set_rect(x, y, w, h)
        label_obj.set_size(cons.MAINMENU_FONTSIZE)
        return label_obj

    def calc_info_box(self, info_obj):
        info_obj.set_size(cons.TILE_D)
        x = (cons.SCREEN_W_PX // 2) + 150
        y = cons.TILE_D * 10
        w = cons.SCREEN_W_PX // 3
        h = cons.SCREEN_H_PX // 2
        info_obj.set_rect(x, y, w, h)
        info_obj.set_color(cons.MAINMENU_SELECTED_COL)
        return info_obj

    def draw_lines(self, surface):
        col = cons.MAINMENU_SELECTED_COL
        x1, y1 = self.text_obj.rect.bottomleft
        x2, y2 = self.text_obj.rect.bottomright
        pg.draw.line(surface, col, (x1, y1), (x2, y2), 1)
        pg.draw.line(surface, col, (x1 + 7, y1 + 7), (x2 - 7, y2 + 7), 1)

    def draw(self, surface):
        color = cons.MAINMENU_DEFAULT_COL
        if self.selected:
            color = cons.MAINMENU_SELECTED_COL
            self.draw_lines(surface)
            self.info_obj.draw(surface)
        self.text_obj.set_color(color)

        # Draw both messages
        self.text_obj.draw(surface)


class MainMenu():
    def __init__(self, screen, statemanager):
        self.statemanager = statemanager
        self.screen = screen
        self.func_name = {"Resume": self.resume, "Editor": self.editor, "Quit": self.quit}
        self.bgcolor = cons.MAINMENU_BGCOL
        self.menu_items = self.generate_menu_items()
        self.current_choice = 0
        self.headline = self.generate_headline()

    def generate_menu_items(self):
        retlist = list()
        label_and_txt = zip(cons.MAINMENU_ITEM_LABELS, cons.MAINMENU_ITEM_INFO)
        for idx, item in enumerate(label_and_txt):
            label = Message(item[0], MsgType.INFO)
            info = Message(item[1], MsgType.INFO)
            retlist.append(MainMenuItem(idx, self.screen, label, info))
            # Set the first menu-item to be selected
            retlist[0].selected = True
        return retlist

    def generate_headline(self):
        headline = Message("Dungeon", MsgType.INFO)
        headline.set_size(cons.TILE_D * 4)
        headline.set_rect(cons.SCREEN_W_PX//12, cons.TILE_D, 400, cons.TILE_D * 2)
        headline.set_color(cons.MAINMENU_DEFAULT_COL)
        return headline

    def up_or_down(self, step):
        """Select next or previous item in the item_list.
        Negative step is down, positive step is up."""
        self.menu_items[self.current_choice].selected = False
        self.current_choice -= step
        self.current_choice %= len(self.menu_items)
        self.menu_items[self.current_choice].selected = True

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
                self.func_name.get(self.menu_items[self.current_choice].text)()

    def resume(self):
        self.statemanager.switch_state('GAME')

    def quit(self):
        self.statemanager.switch_state('EXITING')

    def editor(self):
        print("Editor is forthcoming...")

    def update(self):
        self.handle_events()

    def draw(self):
        self.screen.fill(self.bgcolor)
        self.headline.draw(self.screen)
        for menu_item in self.menu_items:
            menu_item.draw(self.screen)
