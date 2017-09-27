#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
// Local includes
#include "map.h"

// Function declarations 
void log_SDL_error(FILE *output, char *message);
void handle_keypress(SDL_Event event);
void get_input(SDL_Event event);
SDL_Texture *image_loader(char *filename, SDL_Renderer* renderer);
void renderTextureatXY(SDL_Texture *texture, SDL_Renderer *renderer, int x, int y, int size);

// Let the Dungeon begin!
int main(int argc, char** argv){
    int WINDOW_WIDTH;
    int WINDOW_HEIGHT;
    int TILE_SIZE = 16;

    if(argc != 3){
        printf("Usage: ./dungeon <width> <height>\nUsing Width: 1600 Height: 800\n");
        WINDOW_WIDTH = 1200;
        WINDOW_HEIGHT = 608;
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
    int MAP_HEIGHT = WINDOW_HEIGHT_TILES * 0.8;
    int HUD_WIDTH = WINDOW_WIDTH_TILES;
    int HUD_HEIGHT = WINDOW_HEIGHT_TILES - MAP_HEIGHT;
    int MINIMAP_WIDTH = WINDOW_WIDTH_TILES - MAP_WIDTH;
    int MINIMAP_HEIGHT = MAP_HEIGHT; 
    
    // Initialize SDL and setup
    if(SDL_Init(SDL_INIT_VIDEO) < 0){
        log_SDL_error(stdout, "SDL_Init");
        exit(1);
    }
    if(TTF_Init() < 0){
        printf("TTF_Error: %s\n", TTF_GetError());
        exit(1);
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

    // 2D array of int 1s.
    // TODO: Make this independant module.
    int x, y;
    int **dungeon = (int **)malloc(MAP_HEIGHT * sizeof(int *));
    for(y = 0; y < MAP_HEIGHT; y++){
        dungeon[y] = (int *)malloc(MAP_WIDTH * sizeof(int)); 
    }

    // Load some images
    SDL_Texture *white_wall = image_loader("wall_white.bmp", renderer);
    SDL_Texture *red_wall = image_loader("wall_red.bmp", renderer);
    SDL_Texture *blue_wall = image_loader("wall_blue.bmp", renderer);

    // Game loop
    int done = 0;
    SDL_Event event;
    while(!done){
        while(SDL_PollEvent(&event)){
            if((event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_q) || 
                event.type == SDL_QUIT){
                printf("Got QUIT.\n");
                done = 1;
                break;
            }
            get_input(event);
        }
        // Clear
        SDL_RenderClear(renderer);

        // Update
        

        // Draw everything
        for(y = 0; y < MAP_HEIGHT; y++){
            for(x = 0; x < MAP_WIDTH; x++){
                renderTextureatXY(white_wall, renderer, x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE);
            }
        }
        for(y = MAP_HEIGHT; y < MAP_HEIGHT+HUD_HEIGHT; y++){
            for(x = 0; x < HUD_WIDTH; x++){
                renderTextureatXY(red_wall, renderer, x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE);                
            }
        }
        // Blit to minimap surface
        for(y = 0; y < MINIMAP_HEIGHT; y++){
            for(x = MAP_WIDTH; x < MAP_WIDTH+MINIMAP_WIDTH; x++){
                renderTextureatXY(blue_wall, renderer, x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE);                
            }
        }

        // Present
        SDL_RenderPresent(renderer);
    }
    // Cleanup and close
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();
}

// --------------------------------------------------
//                  FUNCTIONS
// --------------------------------------------------

/* image_loader takes a bmp and loads it onto 
   a texture to be handed to the renderer.
*/
SDL_Texture *image_loader(char *filename, SDL_Renderer *renderer){
    SDL_Texture * texture = NULL;
    SDL_Surface *image_surface = SDL_LoadBMP(filename);
    if(NULL != image_surface){
        // Attempt to create texture
        texture = SDL_CreateTextureFromSurface(renderer, image_surface);
        if(texture == NULL){
			log_SDL_error(stdout, "CreateTextureFromSurface");
		}
	}
	else {
		log_SDL_error(stdout, "LoadBMP");
	}
	return texture;
}

/* Renders a given texture to the renderer at 
   position x and y. 
*/
void renderTextureatXY(SDL_Texture *texture, SDL_Renderer *renderer, int x, int y, int size){
    //Setup the destination rectangle to be at the position we want
	SDL_Rect destination;
	destination.x = x;
    destination.y = y;
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
        printf("%d - %s\n", event.key.keysym.sym, SDL_GetKeyName(event.key.keysym.sym));
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