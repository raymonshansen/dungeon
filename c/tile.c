#include <stdlib.h>
#include <stdio.h>
#include "tile.h"

#include <SDL2/SDL.h>

struct tile {
    SDL_Texture* type;
}

/*  Creates an empty default tile.
*/
tile_t *tile_create(void){
    tile_t *newtile = malloc(sizeof(tile_t));
    
    if(newtile){
        newtile->textype = texures[DEFAULT];
    }
    return newtile;
}