#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>

// Local includes
#include "map.h"
#include "tile.h"
#include "tiletypes.h"

// Function declarations
void log_SDL_error(FILE *output, char *message);
void handle_keypress(SDL_Event event);
void get_input(SDL_Event event);
SDL_Texture *image_loader(const char *filename, SDL_Renderer* renderer);
void renderTextureatXY(SDL_Texture *texture, SDL_Renderer *renderer, int x, int y, int size);
void draw_map_hud(SDL_Texture **textures, 
    SDL_Renderer *renderer, 
    int herox, int heroy, 
    map_t *newmap, 
    int MAP_WIDTH, int MAP_HEIGHT, 
    int TILE_SIZE, 
    tiletype_t* map_hud_tiles);
//void draw_map_hud(SDL_Texture **textures, SDL_Renderer *renderer, int herox, int heroy, map_t *newmap, int MAP_WIDTH, int MAP_HEIGHT, int TILE_SIZE);

// Let the Dungeon begin!
int main(int argc, char** argv){
    int WINDOW_WIDTH;
    int WINDOW_HEIGHT;
    int TILE_SIZE = 16;

    if(argc != 3){
        printf("Usage: ./dungeon <width> <height>\nUsing Width: 1600 Height: 800\n");
        WINDOW_WIDTH = 208;
        WINDOW_HEIGHT = 192;
    } else {
        // Window size in pixels
        WINDOW_WIDTH = atoi(argv[1]) - (atoi(argv[1]) % TILE_SIZE);
        WINDOW_HEIGHT = atoi(argv[2]) - (atoi(argv[2]) % TILE_SIZE);
        printf("Width: %d\nHeight: %d\n", WINDOW_WIDTH, WINDOW_HEIGHT);
    }

    // Window size in tiles
    int WINDOW_WIDTH_TILES = WINDOW_WIDTH/TILE_SIZE;
    int WINDOW_HEIGHT_TILES = WINDOW_HEIGHT/TILE_SIZE;

    // Map, hud and minimap sizes.
    int MAP_WIDTH = WINDOW_WIDTH_TILES * 0.7;
    if(MAP_WIDTH % 2 == 0)
        MAP_WIDTH++;
    int MAP_HEIGHT = WINDOW_HEIGHT_TILES * 0.8;
    if(MAP_HEIGHT % 2 == 0)
        MAP_HEIGHT++;
    // Hero position
    int herox = MAP_WIDTH/2;
    int heroy = MAP_HEIGHT/2;
    int HUD_WIDTH = WINDOW_WIDTH_TILES;
    int HUD_HEIGHT = WINDOW_HEIGHT_TILES - MAP_HEIGHT;
    int MINIMAP_WIDTH = WINDOW_WIDTH_TILES - MAP_WIDTH;
    int MINIMAP_HEIGHT = MAP_HEIGHT;

    // Initialize SDL and sub-libraries
    if(SDL_Init(SDL_INIT_VIDEO) < 0){
        log_SDL_error(stdout, "SDL_Init");
        exit(1);
    }
    if(TTF_Init() < 0){
        printf("TTF_Error: %s\n", TTF_GetError());
        exit(1);
    }
    // load support for the JPG and PNG image formats
    if(IMG_Init(IMG_INIT_JPG|IMG_INIT_PNG) < 0) {
        printf("IMG_Init: Failed to init required jpg and png support!\n");
        printf("IMG_Init: %s\n", IMG_GetError());
        // handle error
    }

    SDL_Window *window = SDL_CreateWindow("Dungeon",
                                          SDL_WINDOWPOS_UNDEFINED,
                                          SDL_WINDOWPOS_UNDEFINED,
                                          WINDOW_WIDTH, WINDOW_HEIGHT,
                                          SDL_WINDOW_OPENGL);
    if(NULL == window){
        log_SDL_error(stdout, "SDL_Window");
        exit(1);
    }
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if(NULL == renderer){
        log_SDL_error(stdout, "SDL_Renderer");
        exit(1);
    }
    // Load some images
    SDL_Texture **textures = malloc(TILENUM * sizeof(SDL_Texture*));
    int i;
    for(i = 0; i < TILENUM; i++){
        textures[i] = image_loader(imagefiles[i], renderer);
    }

    // 2D array of int 1s.
    // TODO: Make this independant module.
    int x, y;
    int **dungeon = (int **)malloc(MAP_HEIGHT * sizeof(int *));
    for(y = 0; y < MAP_HEIGHT; y++){
        dungeon[y] = (int *)malloc(MAP_WIDTH * sizeof(int));
    }

    // NEW MAP MODULE!
    map_t* newmap = map_create(15, 15);
    // Make an array to hold the tiletypes that gets printed in the map hud.
    tiletype_t *map_hud_tiles = malloc(MAP_HEIGHT * MAP_WIDTH * sizeof(tiletype_t));
    for(i = 0; i < MAP_HEIGHT * MAP_WIDTH; i++){
        map_hud_tiles[i] = DEFAULT;
    }

    // Game loop
    int done = 0;
    SDL_Event event;
    while(!done){
        while(SDL_PollEvent(&event)){
            if((event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_q) || event.type == SDL_QUIT){
                printf("Got QUIT.\n");
                done = 1;
                break;
            }
            if(event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_m){
                printf("MAP_WIDTH: %d\nMAP_HEIGHT: %d\n", MAP_WIDTH, MAP_HEIGHT);
                continue;
            }
            if(event.type == SDL_KEYDOWN){
                switch(event.key.keysym.sym)
                {
                case SDLK_KP_8:
                case SDLK_UP:
                    heroy -= 1;
                    break;
                case SDLK_KP_2:
                case SDLK_DOWN:
                    heroy += 1;
                    break;
                case SDLK_KP_4:
                case SDLK_LEFT:
                    herox -= 1;
                    break;
                case SDLK_KP_6:
                case SDLK_RIGHT:
                    herox += 1;
                    break;
                default:
                    continue;
                }
            }
            // get_input(event);
        }
        // Clear
        SDL_RenderClear(renderer);

        // Update current_map_hud

        // Draw map hud
        draw_map_hud(textures, renderer, herox, heroy, newmap, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, map_hud_tiles);
        // Draw stat-hud
        for(y = MAP_HEIGHT; y < MAP_HEIGHT+HUD_HEIGHT; y++){
            for(x = 0; x < HUD_WIDTH; x++){
                renderTextureatXY(textures[GREEN], renderer, x, y, TILE_SIZE);
            }
        }
        // Draw message hud
        for(y = 0; y < MINIMAP_HEIGHT; y++){
            for(x = MAP_WIDTH; x < MAP_WIDTH+MINIMAP_WIDTH; x++){
                renderTextureatXY(textures[BLUE], renderer, x, y, TILE_SIZE);
            }
        }

        // Present
        SDL_RenderPresent(renderer);
    }
    // Cleanup and close
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    IMG_Quit();
    TTF_Quit();
    SDL_Quit();
}

// --------------------------------------------------
//                  FUNCTIONS
// --------------------------------------------------

void draw_map_hud(SDL_Texture **textures, 
                  SDL_Renderer *renderer, 
                  int herox, int heroy, 
                  map_t *newmap, 
                  int MAP_WIDTH, int MAP_HEIGHT, 
                  int TILE_SIZE, 
                  tiletype_t* map_hud_tiles){
    int x, y;
    int index = 0;
    // update the tiles in the map hud.
    map_get_hud(herox, heroy, MAP_WIDTH, MAP_HEIGHT, map_hud_tiles, newmap);

    for(y = 0; y < MAP_HEIGHT; y++){
        for(x = 0; x < MAP_WIDTH; x++){
            tiletype_t type = map_hud_tiles[index];
            renderTextureatXY(textures[type], renderer, x, y, TILE_SIZE);
            index++;
        }
    }
}    
/*
void draw_map_hud(SDL_Texture **textures, SDL_Renderer *renderer, int herox, int heroy, map_t *newmap, int MAP_WIDTH, int MAP_HEIGHT, int TILE_SIZE){
    int x = 0;
    int y = 0;
    int mapx;
    int mapy;
    for(y = 0; y < MAP_HEIGHT; y++){
        for(x = 0; x < MAP_WIDTH; x++){
            // Keeping hud within x-boundaries
            if(herox <= (MAP_WIDTH / 2)){
                mapx = x;
            } else if(herox >= map_width(newmap) - (MAP_WIDTH/2)){
                mapx = map_width(newmap) - MAP_WIDTH + x;
            } else {
                mapx = herox - (MAP_WIDTH / 2) + x;
            }
            // Keeping hud within y-boundaries
            if(heroy <= (MAP_WIDTH / 2)){
                mapy = y;
            } else if(heroy >= map_height(newmap) - (MAP_HEIGHT / 2)){
                mapy = map_height(newmap) - MAP_HEIGHT + y;
            } else {
                mapy = heroy - (MAP_HEIGHT / 2) + y;
            }
            // Render current (x,y) of the hud.
            renderTextureatXY(textures[map_get_tiletype(mapx, mapy, newmap)], renderer, x, y, TILE_SIZE);
        }
    }
}
*/


/* image_loader takes a bmp and loads it onto
   a texture to be handed to the renderer.
*/
SDL_Texture *image_loader(const char *filename, SDL_Renderer *renderer){
    printf("Loading %s\n", filename);
    SDL_Texture * texture = NULL;
    SDL_Surface *image_surface = IMG_Load(filename);
    if(NULL != image_surface){
        // Attempt to create texture
        texture = SDL_CreateTextureFromSurface(renderer, image_surface);
        if(texture == NULL){
			log_SDL_error(stdout, "CreateTextureFromSurface");
		}
	}
	else {
		printf("IMG_Error: %s\n", IMG_GetError());
	}
	return texture;
}

/* Renders a given texture to the renderer at
   position x and y.
*/
void renderTextureatXY(SDL_Texture *texture, SDL_Renderer *renderer, int x, int y, int size){
    //Setup the destination rectangle to be at the position we want
	SDL_Rect destination;
	destination.x = x*size;
    destination.y = y*size;
    destination.w = size;
    destination.h = size;
	SDL_RenderCopy(renderer, texture, NULL, &destination);
}


/* Function to handle keypresses and
   call appropriate functions. For now
   it simply prints the key pushed to stdout.
*/
void handle_keypress(SDL_Event event){
    if(event.type == SDL_KEYDOWN){
        return;
        //printf("%d - %s\n", event.key.keysym.sym, SDL_GetKeyName(event.key.keysym.sym));
    }
}

void get_input(SDL_Event event){
    handle_keypress(event);
}

/*
    Generic function that checks the current error
    from SDL and sends it to the FILE-pointer given.
    Usually stdotu.
*/
void log_SDL_error(FILE *output, char *message){
    fprintf(output, "%s, Error: %s\n", message, SDL_GetError());
}