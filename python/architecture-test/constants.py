import pygame

TILE_D = 32

# 1600px
SCREEN_TW = 40
# 960px
SCREEN_TH = 20

# 1280px
MAP_VIEW_TW = int(SCREEN_TW * 0.7)
# 768px
MAP_VIEW_TH = int(SCREEN_TH * 0.8)

STAT_VIEW_TW = MAP_VIEW_TW
STAT_VIEW_TH = SCREEN_TH - MAP_VIEW_TH

LOG_VIEW_TW = SCREEN_TW - MAP_VIEW_TW
LOG_VIEW_TH = SCREEN_TH

MAP_DIM = (TILE_D*MAP_VIEW_TW, TILE_D*MAP_VIEW_TH)
STAT_DIM = (TILE_D*STAT_VIEW_TW, TILE_D*STAT_VIEW_TH)
LOG_DIM = (TILE_D*LOG_VIEW_TW, TILE_D*LOG_VIEW_TH)

MAP_POS = pygame.Rect(0, 0, MAP_DIM[0], MAP_DIM[1])
STAT_POS = pygame.Rect(0, TILE_D*MAP_VIEW_TH, STAT_DIM[0], STAT_DIM[1])
LOG_POS = pygame.Rect(TILE_D*MAP_VIEW_TW, 0, LOG_DIM[0], LOG_DIM[1])

DIRECTIONS = {'NW': (-1, -1),
              'N': (0, -1),
              'NE': (1, -1),
              'W': (-1, 0),
              'E': (1, 0),
              'SW': (-1, 1),
              'S': (0, 1),
              'SE': (1, 1)}
