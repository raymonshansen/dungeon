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

    /*TEST-MAP 0f 15 by 15 tiles*/
    /*
    tiletype_t testmap[] = {WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE, 
                            WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE, 
                            WHITE,WHITE,FLOOR,RED,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,RED,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,RED,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,RED,RED,RED,RED,RED,FLOOR,FLOOR,FLOOR,WHITE,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,FLOOR,RED,FLOOR,FLOOR,WHITE,FLOOR,FLOOR,FLOOR,WHITE,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,FLOOR,RED,FLOOR,FLOOR,WHITE,WHITE,WHITE,WHITE,WHITE,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,FLOOR,RED,FLOOR,FLOOR,RED,WHITE,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,WHITE,FLOOR,RED,FLOOR,FLOOR,RED,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,FLOOR,RED,FLOOR,FLOOR,RED,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,FLOOR,FLOOR,RED,FLOOR,FLOOR,RED,FLOOR,FLOOR,FLOOR,FLOOR,FLOOR,WHITE,WHITE,
                            WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,
                            WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE,WHITE};
    */
    int testmap[] = {1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,6,6,6,6,6,6,6,6,1,0,0,0,0,0,1,6,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,6,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,6,6,6,6,6,6,6,6,1,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,6,6,6,6,6,6,6,6,1,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,6,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,1,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,1,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,1,6,6,6,4,4,6,6,6,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,1,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,1,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,1,1,2,2,2,2,2,2,2,2,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,1,1,2,2,2,2,2,2,2,2,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,2,2,2,2,2,2,2,2,2,2,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,3,3,3,2,2,2,2,2,2,2,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,3,3,3,2,2,2,2,2,3,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,3,2,2,2,2,2,3,3,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,3,2,2,3,6,6,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,6,6,3,3,6,6,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,6,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,};
    map_t *newmap = malloc(sizeof(map_t));
    
    if (newmap){
        //newmap->width = width;
        //newmap->height = height;
        newmap->width = 50;
        newmap->height = 50;
    
        newmap->tilearray = malloc(newmap->width * newmap->height * sizeof(tile_t*));
        int i;
        // Populate the map array with tile pointers.
        for(i = 0; i < newmap->width * newmap->height; i++){
            newmap->tilearray[i] = tile_create();
            if(NULL == newmap->tilearray[i]){
                printf("Error in allocating tile at coordinate (%d, %d).", i % newmap->width, i / newmap->width);
            }
            // Use hard coded testmap and dimensions!
            tile_set_type(newmap->tilearray[i], (tiletype_t)testmap[i]);
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

/*  Returns the tile pointer at a given 
    coordinate of the given map. 
*/
tile_t* map_get_tile(int x, int y, map_t* map){
    tile_t* tile = NULL;
    tile = map->tilearray[x + (y * map->width)];
    return tile;
}

/*  Returns the tile type for a tile
    at the given coordinates of the given map.
*/
tiletype_t map_get_tiletype(int x, int y, map_t* map){
    tile_t* tile = map_get_tile(x, y, map);
    if(!tile){
        return DEFAULT;
    } else {
        return tile_get_type(tile);
    }
}

/*  Takes a pointer to an array which should be 
    updated with the tiletypes_t that fit in the hud with the 
    given width and height. The @ should always be in the middle.
    Cap to corners for now...
*/
void map_get_hud(int herox, int heroy, int hud_width, int hud_height, tiletype_t* tiletypes, map_t *map){
    // Calculate the map coordinates corresponding to the
    // upper left of the hud.
    int hud_start_x = herox - (hud_width/2);
    int hud_start_y = heroy - (hud_height/2);

    int x, y;
    int i = 0;
    for(y = hud_start_y; y < hud_start_y + hud_height; y++){
        for(x = hud_start_x; x < hud_start_x + hud_width; x++){
            // Set to empty tile if hud moves off the edge of the map
            if(x < 0 || x >= map_width(map) || y < 0 || y >= map_height(map)){
                tiletypes[i] = DEFAULT;
            } else {
                tiletypes[i] = map_get_tiletype(x, y, map);
            }
            i++;
        }
    }
    // Hardcode the hero into the middle for now...
    tiletypes[(hud_width * hud_height) / 2] = ATT;
}