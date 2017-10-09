#include <stdlib.h>
#include <stdio.h>
#include "map.h"
#include "tile.h"
#include "tiletypes.h"

struct map {
    // Basic size (expand later...)
    int width;
    int height;

    tile_t** tilearray;
};
/*  Creates a new map with given with and height
    populated with the default tile type.
*/
map_t * map_create(int width, int height){
    map_t *newmap = malloc(sizeof(map_t));
    
    if (newmap){
        newmap->width = width;
        newmap->height = height;
    
        newmap->tilearray = malloc(newmap->width * newmap->height * sizeof(tile_t*));
        int i;
        // Populate the map array with tile pointers.
        for(i = 0; i < newmap->width * newmap->height; i++){
            newmap->tilearray[i] = tile_create();
            if(NULL == newmap->tilearray[i]){
                printf("Error in allocating tile at coordinate (%d, %d).", i % newmap->width, i / newmap->width);
            }
        }
    }
    return newmap;
}

/*  Returns the width of the map
*/
int map_width(map_t *map){
    return map->width;
}

/*  Returns the height of the map
*/
int map_height(map_t *map){
    return map->height;
}

/*  Returns the tile pointer at e given 
    coordinate of the given map.
*/
tile_t* map_get_tile(int x, int y, map_t* map){
    tile_t* tile = NULL;
    if(x > map->width){
        return tile;
    }
    if(y > map->height){
        return tile;
    }
    tile = map->tilearray[x + (y * map->width)];
    if(NULL == tile){
        printf("Map ERROR! No such tile!");
    }
    return tile;
}

/*  Returns the tile type for a tile
    at the given coordinates of the given map.
*/
tiletype_t map_get_tiletype(int x, int y, map_t* map){
    return tile_get_type(map_get_tile(x, y, map));
}