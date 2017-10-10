#include <stdlib.h>
#include <stdio.h>
#include "tile.h"
#include "tiletypes.h"

#include <SDL2/SDL.h>

struct tile {
    tiletype_t texID;
    int size; // All tiles are square
};

/*  Creates an empty default tile.
*/
tile_t *tile_create(void){
    tile_t *newtile = malloc(sizeof(tile_t));
    
    if(newtile){
        newtile->texID = WHITE;
        newtile->size = 16;
    }
    return newtile;
}

/*  Gets the tiletype for a given tile.
*/
tiletype_t tile_get_type(tile_t* tile){
    return tile->texID;
}

/*  tile_set_type
    Sets the tiletype to the fiven type.
    Returns 1 on success and 0 on fail.
*/
int tile_set_type(tile_t* tile, tiletype_t type){
    tile->texID = type;
    return 1;
}