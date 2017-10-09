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
        newtile->texID = DEFAULT;
    }
    return newtile;
}