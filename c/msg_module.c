#include <stdlib.h>
#include <stdio.h>
#include "msg_module.h"
#include "list.h"

/* STRUCT FOR THE MESSAGE MODULE */
struct msg_module{
    int max_messages;
    int updated;
    
    list_t *msg_list;
    // screen variables
    int x;
    int y;
    int width;
    int height;
    SDL_Renderer *renderer;
    SDL_Texture **textures;
    TTF_Font* font;
};

/* STRUCT FOR A MESSAGE*/
struct msg{
    char* text;
};

/*  msg_create returns a pointer to an empty message module ready to use.
    It is able to manage several different types of message-list.
    e.g. DEBUG, BATTLE-LOG, GAMEPLAY, ERROR, NPC-TALK etc...
    Each message is held in its own msg struct containing the actual 
    string of the message along with its font, color, size etc.
*/
msg_module_t *msg_module_create(int x, int y, int width, int height, int max_messages, SDL_Renderer *renderer, SDL_Texture **textures){
    msg_module_t * msg_module = malloc(sizeof(msg_module_t));
    if(!msg_module){
        printf("Error in msg_module_create()");
        return NULL;
    }
    list_t *list = list_create();
    if(!list){
        printf("Error in msg_module_create()");
        return NULL;
    }
    msg_module->font = TTF_OpenFont("arial.ttf", 24);
    if(!msg_module->font){
        printf("Error in msg_module_create()");
        return NULL;
    }
    msg_module->max_messages = max_messages;
    msg_module->updated = 1;
    msg_module->msg_list = list;
    msg_module->x = x;
    msg_module->y = y;
    msg_module->width = width;
    msg_module->height = height;
    msg_module->renderer = renderer;
    msg_module->textures = textures;
    return msg_module;
}

/*  msg_module_draw draws the last x messages of the message list in the given
    area of the screen, with the given renderer. Could perhaps be extended to accomodate
    several types of lists so the player can swap between different message logs.
*/
void msg_module_draw(msg_module_t *msg_module){
    SDL_Color textColor = {255, 255, 255, 0};
    SDL_Surface* surfaceMessage = TTF_RenderText_Solid(msg_module->font, "put your text here", textColor);
    
    SDL_Texture* message = SDL_CreateTextureFromSurface(msg_module->renderer, surfaceMessage);
    SDL_FreeSurface(surfaceMessage);
    SDL_Rect message_rect;
    message_rect.x = msg_module->x; 
    message_rect.y = msg_module->y;
    message_rect.w = msg_module->width;
    message_rect.h = msg_module->height;
    
    SDL_RenderCopy(msg_module->renderer, message, NULL, &message_rect);
    
}

/*  Return the current state of the module. 1 if there are un-drawn messages.
    0 if they have all been drawn.
*/
int msg_module_updated(msg_module_t *msg_module){
    return msg_module->updated;
}
