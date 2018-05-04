import pygame as pg

TILE_D = 32

# 1600px
SCREEN_TW = 40
SCREEN_W_PX = SCREEN_TW * TILE_D
# 960px
SCREEN_TH = 20
SCREEN_H_PX = SCREEN_TH * TILE_D


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

# Font
LOG_FONTSIZE = TILE_D // 2
MAINMENU_FONTSIZE = TILE_D * 2
MAINMENU_BGCOL = pg.color.Color("black")
MAINMENU_DEFAULT_COL = pg.color.Color("antiquewhite")
MAINMENU_SELECTED_COL = pg.color.Color("goldenrod")
