#include <stdlib.h>
#include <stdio.h>
#include "map.h"
#include "tile.h"

struct map {
    // Basic size (expand later...)
    int width;
    int height;

    tile_t* tilearray;
}
/*  Creates a new map with given with and height
    populated with the default tile type.
*/
map_t * map_create(int with, int height){
    map_t *newmap = malloc(sizeof(map_t));
    
    if (newmap){
        newmap->width = width;
        newmap->height = height;
    
        tile_t *tile_array = malloc(newmap->width * newmap->height * sizeof(tile_t));
        int i;
        // Populate the map array.
        for(i = 0; i < newmap->width * newmap->height; i++){
            tile_array[i] = tile_create();
            if(NULL == tile_array[i]){
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