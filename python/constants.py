import pygame as pg

TILE_D = 32

# Comment in for small or big screen

# HD screen
SCREEN_TW, SCREEN_TH = 50, 30
# Low res screen
SCREEN_TW, SCREEN_TH = 35, 20

SCREEN_W_PX = SCREEN_TW * TILE_D

SCREEN_H_PX = SCREEN_TH * TILE_D

SCREEN_SIZE = (SCREEN_W_PX, SCREEN_H_PX)


MAP_VIEW_TW = int(SCREEN_TW * 0.7)
MAP_VIEW_TH = int(SCREEN_TH * 0.8)

STAT_VIEW_TW = MAP_VIEW_TW
STAT_VIEW_TH = SCREEN_TH - MAP_VIEW_TH

LOG_VIEW_TW = SCREEN_TW - MAP_VIEW_TW
LOG_VIEW_TH = SCREEN_TH

MAP_DIM = (TILE_D*MAP_VIEW_TW, TILE_D*MAP_VIEW_TH)
STAT_DIM = (TILE_D*STAT_VIEW_TW, TILE_D*STAT_VIEW_TH)
LOG_DIM = (TILE_D*LOG_VIEW_TW, TILE_D*LOG_VIEW_TH)

MAP_POS = pg.Rect(0, 0, MAP_DIM[0], MAP_DIM[1])
STAT_POS = pg.Rect(0, TILE_D*MAP_VIEW_TH, STAT_DIM[0], STAT_DIM[1])
LOG_POS = pg.Rect(TILE_D*MAP_VIEW_TW, 0, LOG_DIM[0], LOG_DIM[1])

DIRECTIONS = {'NW': (-1, -1),
              'N': (0, -1),
              'NE': (1, -1),
              'W': (-1, 0),
              'E': (1, 0),
              'SW': (-1, 1),
              'S': (0, 1),
              'SE': (1, 1)}
FOUR_DIRECTIONS = {'N': (0, -1),
                   'W': (-1, 0),
                   'E': (1, 0),
                   'S': (0, 1)}

# Font
LOG_FONTSIZE = TILE_D // 2

# Main Menu
MAINMENU_ITEM_LABELS = ["Resume",
                        "Editor",
                        "Quit",
                        ]
MAINMENU_ITEM_INFO = ["Resume the game.",
                      "Switch between 'Game' and 'Editor' mode. This is a future feature not yet implemented.",
                      "Quit the game. Without saving.",
                     ]
MAINMENU_FONTSIZE = TILE_D * 2
MAINMENU_BGCOL = pg.color.Color("black")
MAINMENU_DEFAULT_COL = pg.color.Color("antiquewhite")
MAINMENU_SELECTED_COL = pg.color.Color("goldenrod")
