import sys
import pygame as pg
import random
from utils import round_down
from operator import attrgetter
# Classes
from tiles import Tile
from room import Room
# Needed globals
from config import TILESIZE, ROOMFRAC, MAX_SLICE_OFFSET, Point
"""
A random dungeon generator.
Design based on a simple binary spatial partitioning algorithm.

Follows the following main steps:
1. Start with a space that fits a minimum tile size.
2. Organize the space into a to dimensional list containing tiles.
3. Recursively split into sub-spaces.
4. Fill each smallest space with a randomly shaped room.
5. Randomly dig corridors until there are no unconnected rooms left.

Made by: Raymon Skjørten Hansen, 2017
"""


class Generator():
    """Class to manage the dungeon generator demo."""
    def __init__(self, width, height, recursiondepth):
        """Constructor for the Generator class.

        Caps the desired space to a size that will
        fit the algorithm.
        """
        pg.init()
        # STEP 1: Limit the map fit the necessary specs
        self.width_px = round_down(width, TILESIZE)
        self.height_px = round_down(height, TILESIZE)
        if not (self.width_px//TILESIZE) % 2:
            self.width_px += TILESIZE
        if not (self.height_px//TILESIZE) % 2:
            self.height_px += TILESIZE
        print(f"Width: {self.width_px} Height: {self.height_px}")
        self.rec_depth = recursiondepth
        min_space_in_px = min(self.width_px//ROOMFRAC, self.width_px//ROOMFRAC)
        # minimum number of tiles that the side of a space can have.
        self.min_space = round_down(min_space_in_px//TILESIZE, TILESIZE)
        # Setup the screen etc.
        self.screen = pg.display.set_mode((self.width_px, self.height_px))
        self.width_tiles = self.width_px//TILESIZE
        self.height_tiles = self.height_px//TILESIZE
        print(f"Width: {self.width_tiles} Height: {self.height_tiles}")
        pg.display.set_caption("Dungeon Generator")
        self.screen.fill(pg.color.THECOLORS["black"])
        self.done = False

    def setup(self):
        """STEP 2: Sets up the two dimentional list of tiles"""
        print("Generating tiles...")
        # List of calculated spaces and the rooms
        self.spacelist = []
        self.roomlist = []
        self.corridorlist = []
        self.wall_image = pg.image.load("wall2.png").convert_alpha()
        self.wall_image = pg.transform.scale(self.wall_image, (TILESIZE, TILESIZE))
        self.floor_image = pg.image.load("floor2.png").convert_alpha()
        self.floor_image = pg.transform.scale(self.floor_image, (TILESIZE, TILESIZE))
        self.hordoor = pg.image.load("hor_door.png").convert_alpha()
        self.hordoor = pg.transform.scale(self.hordoor, (TILESIZE, TILESIZE))
        self.vertdoor = pg.image.load("vert_door.png").convert_alpha()
        self.vertdoor = pg.transform.scale(self.vertdoor, (TILESIZE, TILESIZE))
        self.rockimage = pg.image.load("rock.png").convert_alpha()
        self.rockimage = pg.transform.scale(self.rockimage, (TILESIZE, TILESIZE))
        self.enterimage = pg.image.load("enter.png").convert_alpha()
        self.enterimage = pg.transform.scale(self.enterimage, (TILESIZE, TILESIZE))
        self.exitimage = pg.image.load("exit.png").convert_alpha()
        self.exitimage = pg.transform.scale(self.exitimage, (TILESIZE, TILESIZE))
        self.playerimage = pg.image.load("alfa.png").convert_alpha()
        self.playerimage = pg.transform.scale(self.playerimage, (TILESIZE, TILESIZE))
        self.map = [[Tile(w*TILESIZE, h*TILESIZE, 0, self.rockimage, self.wall_image, self.floor_image, self.vertdoor, self.hordoor, self.enterimage, self.exitimage, self.playerimage) for h in range(self.height_tiles)] for w in range(self.width_tiles)]
        self.playerx = 0
        self.playery = 0
        self.new_level_x = 0
        self.new_level_y = 0
        print("Done")

    def handle_events(self):
        """Method for handling input/output events"""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.done = True
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.done = True
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.spacelist.clear()
                print("Running BSP...")
                vert = False
                if (self.width_tiles > self.height_tiles):
                    vert = True
                self.split_space(0, 0, self.width_tiles, self.height_tiles, vert, 0)
                print("Done")
            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                i = 0
                for spaceparam in self.spacelist:
                    x, y, width, height = spaceparam
                    for col in range(x, x+width):
                        for row in range(y, y+height):
                            self.map[col][row].draw_tile(self.screen)
                    i += 1
            if event.type == pg.KEYDOWN and event.key == pg.K_y:
                self.roomlist.clear()
                self.reset_map()
                self.spawn_rooms()
                self.enter_exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.maze()
            if event.type == pg.KEYDOWN and event.key == pg.K_n:
                self.remove_dead_ends()
            if event.type == pg.KEYDOWN and event.key == pg.K_b:
                self.build_walls()
            if event.type == pg.KEYDOWN and event.key == pg.K_d:
                self.draw_map()
            if event.type == pg.KEYDOWN and event.key == pg.K_l:
                self.new_level()
            if event.type == pg.KEYDOWN and event.key == pg.K_KP8:
                self.move_player("n")                 
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.move_player("n")
            if event.type == pg.KEYDOWN and event.key == pg.K_KP2:
                self.move_player("s")
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.move_player("s")
            if event.type == pg.KEYDOWN and event.key == pg.K_KP6:
                self.move_player("e")
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.move_player("e")
            if event.type == pg.KEYDOWN and event.key == pg.K_KP4:
                self.move_player("w")
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.move_player("w")
            if event.type == pg.KEYDOWN and event.key == pg.K_KP7:
                self.move_player("nw")
            if event.type == pg.KEYDOWN and event.key == pg.K_KP9:
                self.move_player("ne")
            if event.type == pg.KEYDOWN and event.key == pg.K_KP3:
                self.move_player("se")
            if event.type == pg.KEYDOWN and event.key == pg.K_KP1:
                self.move_player("sw")

    def check_level(self, x, y):
        if x == self.new_level_x and y == self.new_level_y:
            self.new_level()

    def move_player(self, direction):
        """Move the player in a direction"""
        if direction is "n":
            if not self.map[self.playerx][self.playery-1].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx][self.playery-1].player = True
                self.map[self.playerx][self.playery-1].draw_tile(self.screen)
                self.playery -= 1
        if direction is "nw":
            if not self.map[self.playerx-1][self.playery-1].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx-1][self.playery-1].player = True
                self.map[self.playerx-1][self.playery-1].draw_tile(self.screen)
                self.playery -= 1
                self.playerx -= 1
        if direction is "ne":
            if not self.map[self.playerx+1][self.playery-1].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx+1][self.playery-1].player = True
                self.map[self.playerx+1][self.playery-1].draw_tile(self.screen)
                self.playery -= 1
                self.playerx += 1
        if direction is "s":
            if not self.map[self.playerx][self.playery+1].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx][self.playery+1].player = True
                self.map[self.playerx][self.playery+1].draw_tile(self.screen)
                self.playery += 1
        if direction is "sw":
            if not self.map[self.playerx-1][self.playery+1].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx-1][self.playery+1].player = True
                self.map[self.playerx-1][self.playery+1].draw_tile(self.screen)
                self.playery += 1
                self.playerx -= 1
        if direction is "se":
            if not self.map[self.playerx+1][self.playery+1].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx+1][self.playery+1].player = True
                self.map[self.playerx+1][self.playery+1].draw_tile(self.screen)
                self.playery += 1
                self.playerx += 1
        if direction is "w":
            if not self.map[self.playerx-1][self.playery].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx-1][self.playery].player = True
                self.map[self.playerx-1][self.playery].draw_tile(self.screen)
                self.playerx -= 1
        if direction is "e":
            if not self.map[self.playerx+1][self.playery].is_wall:
                self.map[self.playerx][self.playery].player = False
                self.map[self.playerx][self.playery].draw_tile(self.screen)
                self.map[self.playerx+1][self.playery].player = True
                self.map[self.playerx+1][self.playery].draw_tile(self.screen)
                self.playerx += 1
        self.check_level(self.playerx, self.playery)

    def new_level(self):
        self.spacelist.clear()
        self.roomlist.clear()
        self.corridorlist.clear()
        self.reset_map()
        vert = False
        if (self.width_tiles > self.height_tiles):
            vert = True
        self.split_space(0, 0, self.width_tiles, self.height_tiles, vert, 0)
        self.spawn_rooms()
        self.enter_exit()
        self.draw_map()
        self.maze()
        self.remove_dead_ends()
        self.build_walls()

    def reset_map(self):
        for x in range(self.width_tiles):
            for y in range(self.height_tiles):
                self.map[x][y].__init__(x*TILESIZE, y*TILESIZE, 0, self.rockimage, self.wall_image, self.floor_image, self.vertdoor, self.hordoor, self.enterimage, self.exitimage, self.playerimage)

    def draw_map(self):
        """Draws all tiles in the map"""
        for x in range(self.width_tiles):
            for y in range(self.height_tiles):
                self.map[x][y].draw_tile(self.screen)

    def calc_padding(self, distance):
        """Calculates an offset from a slice-point.
        Return the offset as number of tiles."""
        percent = random.randint(0, MAX_SLICE_OFFSET)/100
        padding = int(distance*percent)
        return round_down(padding, 1)

    def slicing(self, start, distance, padding):
        """Calculate a spot to do a slice along
        the given distance. Return number of the tile."""
        if random.randint(0, 1):
            slicing = start + (distance // 2) - padding
        else:
            slicing = start + (distance // 2) + padding
        return round_down(slicing, 1)

    def split_space(self, startx, starty, width, height, vertical, depth):
        """STEP 3: Recursively split into smaller sub-spaces
        until each sub-space fits the specifications or it
        reaches the maximum recursion depth.

        Returns a list of the final spaces.
        """
        # Return-conditions: too small rooms or maxdepth
        con1 = width < random.randint(self.width_tiles//8, self.width_tiles//5)
        con2 = height < random.randint(self.width_tiles//8, self.width_tiles//5)
        con3 = depth == self.rec_depth
        if (con1 or con2 or con3):
            # Store all we need to know about a space
            # Constrain space
            if not (startx + 1) % 2:
                startx += 1
            else:
                startx += 2
            if not (starty + 1) % 2:
                starty += 1
            else:
                starty += 2
            if not (width - 3) % 2:
                width -= 3
            else:
                width -= 4
            if not (height - 3) % 2:
                height -= 3
            else:
                height -= 4
            spaceparam = (startx, starty, width, height)
            self.spacelist.append(spaceparam)
            return
            # Keep slicing alternate directions
        else:
            if vertical:
                padding = self.calc_padding(width)
                slicex = self.slicing(startx, width, padding)
                # Calculate sub-space width
                left_width = slicex - startx
                right_width = width - left_width
                # Dig deeper in both sub-spaces
                # LEFT:
                self.split_space(startx, starty, left_width, height, False, depth+1)
                # RIGHT:
                self.split_space(slicex, starty, right_width, height, False, depth+1)
            else:
                padding = self.calc_padding(height)
                slicey = self.slicing(starty, height, padding)
                # Calculate sub-space height
                upper_height = slicey - starty
                lower_height = height - upper_height
                # Dig deeper in both sub-spaces
                # UPPER:
                self.split_space(startx, starty, width, upper_height, True, depth+1)
                # LOWER:
                self.split_space(startx, slicey, width, lower_height, True, depth+1)

    def validate(self, x, y, space):
        if x >= (space[0] + space[2]) or x <= space[0]:
            return False
        if y >= (space[1] + space[3]) or y <= space[1]:
            return False
        if self.map[x][y].dug:
            return False
        return True

    def recursive_dig(self, x, y, space, pointlist):
        if not self.food:
            return
        # Define the eight possible directions to go
        north = Point(x, y-1)
        south = Point(x, y+1)
        west = Point(x-1, y)
        east = Point(x+1, y)
        northwest = Point(x-1, y-1)
        northeast = Point(x+1, y-1)
        southwest = Point(x-1, y+1)
        southeast = Point(x+1, y+1)
        # weirddirections = [northwest, northeast, southwest, southeast]
        # Put them in a list for random pick
        directions = [north, south, west, east]
        # Check in a random direction...
        if random.randint(0, 100) < 5:
            pass
            # directions += weirddirections
        random.shuffle(directions)
        for point in directions:
            if not self.food:
                return
            # If its allowed to dig
            if self.validate(point.x, point.y, space):
                self.map[point.x][point.y].dug = True
                self.map[point.x][point.y].is_wall = False
                self.food = self.food - 1
                pointlist.append(point)
                self.recursive_dig(point.x, point.y, space, pointlist)
        return

    def spawn_rooms(self):
        """Populate each space with a room that fits within
        its constraints. Perhaps pick randomly from a list
        of shapes?
        Return a list of these room-objects"""
        for index, space in enumerate(self.spacelist):
            x, y, w, h = space
            # How many tiles should be dug?
            self.food = (w*h)//4
            if self.food <= 4:
                self.food = 4
            # Pick a point to start digging
            seedx = (x + (w//2))
            seedy = (y + (h//2))
            space = (x, y, w, h)
            # Make a list to fill with points
            pointlist = list()
            self.recursive_dig(seedx, seedy, space, pointlist)
            tiles_in_room = list()
            for point in pointlist:
                self.map[point.x][point.y].id = index
                tiles_in_room.append(self.map[point.x][point.y])
            if pointlist:
                # Mark the space not allowed to dig
                smallestx = sorted(tiles_in_room, key=attrgetter('pos.x'))[0].pos.x//TILESIZE 
                greatestx = sorted(tiles_in_room, key=attrgetter('pos.x'), reverse=True)[0].pos.x//TILESIZE
                smallesty = sorted(tiles_in_room, key=attrgetter('pos.y'))[0].pos.y//TILESIZE
                greatesty = sorted(tiles_in_room, key=attrgetter('pos.y'), reverse=True)[0].pos.y//TILESIZE
                for x in range(smallestx-1, greatestx+2):
                    for y in range(smallesty-1, greatesty+2):
                        self.map[x][y].space = True
                # Finally add the individual rooms to the list of rooms
                self.roomlist.append(Room(tiles_in_room, index, self.map))

    def enter_exit(self):
        """Set enter/exit points"""
        startroom = random.choice(self.roomlist)
        exitroom = random.choice(self.roomlist)
        while exitroom is startroom:
            exitroom = random.choice(self.roomlist)
        starttile = random.choice(startroom.tiles)
        starttile.enter = True
        starttile.player = True
        self.playerx = starttile.pos.x // TILESIZE
        self.playery = starttile.pos.y // TILESIZE
        endtile = random.choice(exitroom.tiles)
        endtile.exit = True
        self.new_level_x = endtile.pos.x // TILESIZE
        self.new_level_y = endtile.pos.y // TILESIZE

    def candig_list(self, x, y):
        """Takes in tile coordinates and returns one list of its
        valid neighbours, or None if we're off grid.
        Also returns a list of the tiles to be dug to get to the valid
        neighbours.
        """
        neighbours = list()
        candig = list()
        north = True
        south = True
        west = True
        east = True
        # Check if its inside the map
        if (x*TILESIZE)-(TILESIZE*2) < 0:
            west = False
        if (x*TILESIZE)+(TILESIZE*2) >= self.width_px:
            east = False
        if (y*TILESIZE)-(TILESIZE*2) < 0:
            north = False
        if (y*TILESIZE)+(TILESIZE*2) >= self.height_px:
            south = False
        # Now that we are inside the map...
        # The neighbours must also not have been dug before
        if west:
            if not self.map[x-2][y].dug and not self.map[x-1][y].dug:
                if not self.map[x-2][y].space and not self.map[x-1][y].space:
                    neighbours.append(self.map[x-2][y])
                    candig.append(self.map[x-1][y])
        if east:
            if not self.map[x+2][y].dug and not self.map[x+1][y].dug:
                if not self.map[x+2][y].space and not self.map[x+1][y].space:
                    neighbours.append(self.map[x+2][y])
                    candig.append(self.map[x+1][y])
        if north:
            if not self.map[x][y-2].dug and not self.map[x][y-1].dug:
                if not self.map[x][y-2].space and not self.map[x][y-1].space:
                    neighbours.append(self.map[x][y-2])
                    candig.append(self.map[x][y-1])
        if south:
            if not self.map[x][y+2].dug and not self.map[x][y+1].dug:
                if not self.map[x][y+2].space and not self.map[x][y+1].space:
                    neighbours.append(self.map[x][y+2])
                    candig.append(self.map[x][y+1])
        # Return both lists
        return neighbours, candig

    def maze_runner(self, startx, starty):
        """An iterative maze carver."""
        # STEP 1: Make an empty list of tiles
        cells = list()
        # STEP 2: Add a tile.
        cells.append(self.map[startx][starty])
        while cells:
            # Pick a tile and dig it
            current = random.choice(cells)
            current.carve(self.screen)
            # Keep tabs of all carved corridor tiles
            self.corridorlist.append(current)
            # Get valid neighbours if any and the tiles to dig in between
            neighbours, candig = self.candig_list(current.pos.x//TILESIZE, current.pos.y//TILESIZE)
            if not neighbours:
                cells.remove(current)
            else:
                index = random.randint(0, len(neighbours)-1)
                neighbours[index].carve(self.screen)
                candig[index].carve(self.screen)
                self.corridorlist.append(candig[index])
                cells.append(neighbours[index])

    def carve_doors(self):
        """Goes through the possible entry points for each room
        and connects some of them to the main corridor."""
        for room in self.roomlist:
            westerndoors = list()
            easterndoors = list()
            northerndoors = list()
            southerndoors = list()
            alldoors = list()
            for entry in room.entry:
                x = entry.pos.x//TILESIZE
                y = entry.pos.y//TILESIZE
                if x - 2 > 0:
                    west = self.map[x-2][y]
                    if west.corridor:
                        westerndoors.append(self.map[x-1][y])
                if x + 2 < self.width_tiles:
                    east = self.map[x+2][y]
                    if east.corridor:
                        easterndoors.append(self.map[x+1][y])
                if y - 2 > 0:
                    north = self.map[x][y-2]
                    if north.corridor:
                        self.map[x][y-1].door_image = self.map[x][y-1].hor_door
                        northerndoors.append(self.map[x][y-1])
                if y + 2 < self.height_tiles:
                    south = self.map[x][y+2]
                    if south.corridor:
                        self.map[x][y+1].door_image = self.map[x][y+1].hor_door
                        southerndoors.append(self.map[x][y+1])
            if westerndoors:
                alldoors.append(westerndoors)
            if easterndoors:
                alldoors.append(easterndoors)
            if northerndoors:
                alldoors.append(northerndoors)
            if southerndoors:
                alldoors.append(southerndoors)
            # Pick one door on each side and connect to corridor.
            for doorslist in alldoors:
                tile = random.choice(doorslist)
                tile.is_door = True
                tile.is_wall = False
                tile.dug = True
                tile.corridor = False
                tile.draw_tile(self.screen)

    def is_dead_end(self, tile):
        """Returns true if the tile is a dead end"""
        x = tile.pos.x//TILESIZE
        y = tile.pos.y//TILESIZE
        i = 0
        if self.map[x][y-1].dug:
            i+=1
        if self.map[x][y+1].dug:
            i+=1
        if self.map[x-1][y].dug:
            i+=1
        if self.map[x+1][y].dug:
            i+=1
        return 0 < i < 2

    def remove_dead_ends(self):
        """Removes some of the dead ends of the maze"""
        done = False
        while not done:
            done = True
            # Check for dead ends
            for tile in self.corridorlist:
                if self.is_dead_end(tile):
                    # Unncarve and remove the tile
                    tile.uncarve(self.screen)
                    self.corridorlist.remove(tile)
                    # Keep checking
                    done = False
        print("Dead ends removed")

    def maze(self):
        """Attempts to carve out all "dead" space
        between the rooms. Then it places doors.
        One on each possible side of a room.
        """
        self.maze_runner(1, 1)
        self.carve_doors()

    def build_walls(self):
        """All non-dug tiles adjacent to a dug tile
        should be a wall"""
        for x in range(1, self.width_tiles-1):
            for y in range(1, self.height_tiles-1):
                tile = self.map[x][y]
                n = self.map[x][y-1]
                nw = self.map[x-1][y-1]
                ne = self.map[x+1][y-1]
                s = self.map[x][y+1]
                sw = self.map[x-1][y+1]
                se = self.map[x+1][y+1]
                w = self.map[x-1][y]
                e = self.map[x+1][y]
                if not tile.dug:
                    if n.dug or nw.dug or ne.dug or s.dug or sw.dug or se.dug or w.dug or e.dug:
                        tile.is_wall = True
                        tile.dug = False
                        tile.draw_tile(self.screen)
        # Top row...
        for x in range(1, self.width_tiles-1):
            tile = self.map[x][0]
            s = self.map[x][1]
            sw = self.map[x-1][1]
            se = self.map[x+1][1]
            if not tile.dug:
                if s.dug or sw.dug or se.dug:
                    tile.is_wall = True
                    tile.dug = False
                    tile.draw_tile(self.screen)
        # Bottom row...
        for x in range(1, self.width_tiles-1):
            tile = self.map[x][self.height_tiles-1]
            n = self.map[x][self.height_tiles-2]
            nw = self.map[x-1][self.height_tiles-2]
            ne = self.map[x+1][self.height_tiles-2]
            if not tile.dug:
                if n.dug or nw.dug or ne.dug:
                    tile.is_wall = True
                    tile.dug = False
                    tile.draw_tile(self.screen)
        # Left side...
        for y in range(1, self.height_tiles-1):
            tile = self.map[0][y]
            e = self.map[1][y]
            se = self.map[1][y+1]
            ne = self.map[1][y-1]
            if not tile.dug:
                if e.dug or se.dug or ne.dug:
                    tile.is_wall = True
                    tile.dug = False
                    tile.draw_tile(self.screen)
        # Right side...
        for y in range(1, self.height_tiles-1):
            tile = self.map[self.width_tiles-1][y]
            w = self.map[self.width_tiles-2][y]
            sw = self.map[self.width_tiles-2][y+1]
            nw = self.map[self.width_tiles-2][y-1]
            if not tile.dug:
                if w.dug or sw.dug or nw.dug:
                    tile.is_wall = True
                    tile.dug = False
                    tile.draw_tile(self.screen)
        # Corners, wow there must be a better way of doing this...
        tile = self.map[0][0]
        if self.map[1][1].dug or self.map[1][0].dug or self.map[0][1].dug:
            tile.is_wall = True
            tile.dug = False
            tile.draw_tile(self.screen)

    def run(self):
        """Main loop to get input and quit"""
        # Setup stuff
        self.setup()
        while not self.done:
            self.handle_events()
            pg.display.update()
        pg.quit()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python dungeon.py <width> <height> <recursion_depth>")
        print("There will be 2**<recursion_depth> number of rooms!")
        exit()
    gen = Generator(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    gen.run()
