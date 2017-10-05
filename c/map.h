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
struct map;
typedef struct map map_t;

/*  map_create()
    Creates an empty map with which 
    the dungeon module can use to construct
    a random dungeon.
*/
    map_t *map_create(int with, int height, int wpad, int hpad);

#endif /* MAP_H_ */