#include <stdlib.h>
#include <stdio.h>
#include "map.h"

struct map {
    // Basic size (expand later...)
    int width;
    int height;
    int wpad;
    int hpad;


}
/* Creates a new map with given with and padding.
*/
map_t * map_create(int with, int height, int wpad, int hpad){
    // Allocate memory for the map
    map_t *newmap = (map_t*)malloc(sizeof(map_t));
    
    if (NULL == newmap){
        printf("Error in allocating space for map.");
        return 0;
    }
    // Set the given size before making space
    newmap->width = width;
    newmap->height = height;
    newmap->wpad = wpad;
    newmap->hpad = hpad;
    // The basic data-structure for the tiles is an array
    int **map = (int**)malloc(height * sizeof(int*));
    for(y = 0; y < height; y++){
        map[y] = (int*)malloc(width * sizeof(int));
    }
    // Populate
    for(y = 0; y < height; y++){
        for(x = 0; x < width; x++){
            map[y][x] = 1;
            printf("(%d, %d), ", x, y);
        }
        printf("\n");
    }
}