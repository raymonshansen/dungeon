#ifndef TILE_H_
#define TILE_H_

#include "tiletypes.h"

/*  The tile is the smallest map unit.
    They contain all necessary information 
    about each tile. Provides the interface 
    the map will use to interact with individual 
    tiles in the map. Typically changing types
    quickly, getting lists of items on a tile etc.

    Tile interface:
*/

typedef struct tile tile_t;

/*  tile_create
    Creates a default tile with no content.
    It's considered "bedrock" or "void".
*/
tile_t* tile_create(void);

/*  tile_set_type
    Sets the tiletype to the fiven type.
    Returns 1 on success and 0 on fail.
*/
int tile_set_type(tile_t* tile, tiletype_t type);

/*  tile_get_type
    Returns the tiletype of a given tile.
*/
tiletype_t tile_get_type(tile_t* tile);

/*  tile_set_description
    Sets the description for the given tile.
    Returns 1 on success and 0 on fail.
*/
int tile_set_description(tile_t* tile, const char* desc);

/*  tile_get_description
    Returns the string description of a given tile.
*/
const char* tile_get_description(tile_t* tile);

#endif /* TILE_H_ */