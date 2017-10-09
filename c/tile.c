#include <stdlib.h>
#include <stdio.h>
#include "tile.h"
#include "tiletypes.h"

#include <SDL2/SDL.h>

struct tile {
    tiletype_t texID;
};

/*  Creates an empty default tile.
*/
tile_t *tile_create(void){
    tile_t *newtile = malloc(sizeof(tile_t));
    
    if(newtile){
        newtile->texID = WHITE;
    }
    return newtile;
}

/*  Gets the tiletype for a given tile.
*/
tiletype_t tile_get_type(tile_t* tile){
    return tile->texID;
}