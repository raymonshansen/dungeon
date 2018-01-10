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

/*  map_get_tile_desc
    Returns the tile description of a given coordinate
*/
const char* map_get_tile_desc(int x, int y, map_t* map);

/*  Take a pointer to tiltype_t and fill with the types 
    that fits within the map-hud size given @s coordinates.
    From the engine/drawing side of things, this pointer will 
    be the same each time, this function just updates the tiletypes
    in it. 
    It might also have options of how those tiletypes are gotten.
    It might or might not stick to edges depending on what looks
    or feels best.
*/
void map_get_hud(int herox, int heroy, int hud_width, int hud_height, tiletype_t* tiletypes, map_t *map);

#endif /* MAP_H_ */