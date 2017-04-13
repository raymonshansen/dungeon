import random
import sys
from collections import namedtuple
import pygame as pg

# Point declaration
Point = namedtuple("Point", ["x", "y"])

# Minimum roomsize
ROOMFRAC = 20
# Corridor width
TILESIZE = 16
# Maximum slice offset from middle
MAX_SLICE_OFFSET = 20
MAX_SPACE_SHRINKAGE = 80
MIN_SPACE_SHRINKAGE = 10
# Coloras
colors = [pg.color.THECOLORS["red"],
          pg.color.THECOLORS["blue"],
          pg.color.THECOLORS["green"],
          pg.color.THECOLORS["purple"],
          pg.color.THECOLORS["yellow"],
          pg.color.THECOLORS["cornflowerblue"],
          pg.color.THECOLORS["chocolate1"],
          pg.color.THECOLORS["deeppink1"],
          pg.color.THECOLORS["greenyellow"],
          pg.color.THECOLORS["powderblue"],
          pg.color.THECOLORS["gold"],
          pg.color.THECOLORS["lightskyblue"],
          pg.color.THECOLORS["lightgreen"],
          pg.color.THECOLORS["paleturquoise4"],
          pg.color.THECOLORS["peachpuff"],
          pg.color.THECOLORS["tan3"], ]
