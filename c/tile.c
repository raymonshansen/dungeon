#include <stdlib.h>
#include <stdio.h>
#include "tile.h"
#include "tiletypes.h"

#include <SDL2/SDL.h>

struct tile {
    tiletype_t texID;
    int size; // All tiles are square
    const char *description;
};

/*  Creates an empty default tile.
*/
tile_t *tile_create(void){
    tile_t *newtile = malloc(sizeof(tile_t));
    
    if(newtile){
        newtile->texID = WHITE;
        newtile->size = 16;
        newtile->description = "Blank";
    }
    return newtile;
}

/*  Gets the tiletype for a given tile.
*/
tiletype_t tile_get_type(tile_t* tile){
    if(!tile){
        return DEFAULT;
    } else {
        return tile->texID;
    }
}

/*  tile_set_type
    Sets the tiletype to the fiven type.
    Returns 1 on success and 0 on fail.
*/
int tile_set_type(tile_t* tile, tiletype_t type){
    tile->texID = type;
    return 1;
}

/*  tile_set_description
    Sets the description for the given tile.
    Returns 1 on success and 0 on fail.
*/
int tile_set_description(tile_t* tile, const char* desc){
    tile->description = desc;
    return 1;
}

/*  tile_get_description
    Returns the string description of a given tile.
*/
const char* tile_get_description(tile_t* tile){
    return tile->description;
}
