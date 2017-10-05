#include <stdlib.h>
#include <stdio.h>
#include "map.h"

struct map {
    // Basic size (expand later...)
    int width;
    int height;

    // Will be array of tile_t structs later...
    int* tilearray;
}
/*  Creates a new map with given with and height.
*/
map_t * map_create(int with, int height){
    // Allocate memory for the map
    map_t *newmap = (map_t*)malloc(sizeof(map_t));
    
    if (NULL == newmap){
        printf("Error in allocating space for map.");
        return 0;
    }
    // Set the given size before making space
    newmap->width = width;
    newmap->height = height;
    // The basic data-structure for the tiles is an array
    // Array of ints for now...
    int *tile_array = (int*)malloc(newmap->width * newmap->height * sizeof(int));

    return newmap;
}

/*  Returns the width of the map
*/
int map_width(map_t *map){
    return map->width;
}


/*  Returns the width of the map
*/
int map_height(map_t *map){
    return map->height;
}