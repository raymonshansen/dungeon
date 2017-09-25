#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>

// Function declarations 
void log_SDL_error(FILE *output, char *message);
void handle_keypress(SDL_Event event);
void get_input(SDL_Event event);
SDL_Surface *image_loader(char *filename);

// Let the Dungeon begin!
int main(int argc, char** argv){
    int WINDOW_WIDTH;
    int WINDOW_HEIGHT;
    if(argc != 3){
        printf("Usage: ./dungeon <width> <height>\nUsing Width: 1600 Height: 800\n");
        WINDOW_WIDTH = 1200;
        WINDOW_HEIGHT = 608;
    } else {
        // Window size in pixels
        WINDOW_WIDTH = atoi(argv[1]) - (atoi(argv[1]) % 16);
        WINDOW_HEIGHT = atoi(argv[2]) - (atoi(argv[2]) % 16);
        printf("Width: %d\nHeight: %d\n", WINDOW_WIDTH, WINDOW_HEIGHT);
    }

    // Window size in tiles
    int WINDOW_WIDTH_TILES = WINDOW_WIDTH/16;
    int WINDOW_HEIGHT_TILES = WINDOW_HEIGHT/16;

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

    SDL_Surface *window_surface = SDL_GetWindowSurface(window);
    
    // Load some images
    //SDL_Surface *att_img = image_loader("att.bmp");
    //SDL_Surface *floor_img = image_loader("floor.bmp");
    SDL_Surface *white_wall = image_loader("wall_white.bmp");
    SDL_Surface *red_wall = image_loader("wall_red.bmp");
    SDL_Surface *blue_wall = image_loader("wall_blue.bmp");
    
    // Blit to map surface
    for(y = 0; y < MAP_HEIGHT; y++){
        for(x = 0; x < MAP_WIDTH; x++){
            SDL_Rect rect = {x*16, y*16, 16, 16};
            SDL_BlitSurface(blue_wall, NULL , window_surface, &rect);
        }
    }
    // Blit to hud surface
    for(y = MAP_HEIGHT; y < MAP_HEIGHT+HUD_HEIGHT; y++){
        for(x = 0; x < HUD_WIDTH; x++){
            SDL_Rect rect = {x*16, y*16, 16, 16};
            SDL_BlitSurface(red_wall, NULL , window_surface, &rect);
        }
    }
    // Blit to minimap surface
    for(y = 0; y < MINIMAP_HEIGHT; y++){
        for(x = MAP_WIDTH; x < MAP_WIDTH+MINIMAP_WIDTH; x++){
            SDL_Rect rect = {x*16, y*16, 16, 16};
            SDL_BlitSurface(white_wall, NULL, window_surface, &rect);
        }
    }
    
    SDL_Texture *window_texture = SDL_CreateTextureFromSurface(renderer, window_surface);

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
        SDL_RenderCopy(renderer, window_texture, NULL, NULL);

        // Present
        SDL_RenderPresent(renderer);
    }
    // Cleanup and close
    printf("Exiting...\n");
    SDL_DestroyTexture(window_texture);
    SDL_FreeSurface(window_surface);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();
}

SDL_Surface *image_loader(char *filename){
    SDL_Surface *image_surface = SDL_LoadBMP(filename);
    if(NULL == image_surface){
        printf("Failed to load %s. SDL_Error: %s\n", filename, SDL_GetError());
        exit(1);
    } else {
        return image_surface;
    }
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