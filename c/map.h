#ifndef MAP_H_
#define MAP_H_

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

#endif /* MAP_H_ */