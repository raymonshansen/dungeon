#ifndef MAP_H_
#define MAP_H_

#include "tile.h"
#include "tiletypes.h"

/*  The map will be an abstract data-structure
    with a lot of support functions. The map
    will likely be a huge struct containing 
    flags and information about itself.
    
    Set up as an array of tiles.

    It will have a lot of support functions enabling
    the interaction with the map done in the game engine.

    Map interface:
*/
typedef struct map map_t;

/*  map_create()
    Creates an empty map with which 
    the dungeon module can use to construct
    a random dungeon.
*/
map_t *map_create(int width, int height);

/*  map_width
    param:
    map_t* - pointer to an existing map
    Returns: the width of the map
*/
int map_width(map_t *map);

/*  map_height
    param:
    map_t* - pointer to an existing map
    Returns: the height of the map
*/
int map_height(map_t *map);

/*  Returns the tile pointer at e given 
    coordinate of the given map.
*/
tile_t* map_get_tile(int x, int y, map_t* map);

/*  Returns the tile type for a tile
    at the given coordinates of the given map.
*/
tiletype_t map_get_tiletype(int x, int y, map_t* map);

tiletype_t* map_get_hud(int herox, int heroy, int MAP_WIDTH, int MAP_HEIGHT, map_t* map);

#endif /* MAP_H_ */