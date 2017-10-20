#include <stdlib.h>
#include <stdio.h>
#include "msg.h"
#include "list.h"

struct msg{
    int max_messages;
    
    list_t *msg_list;
    // screen variables
    int x;
    int y;
    int width;
    int height;
    SDL_Renderer *renderer;
};

/*  msg_create returns a pointer to
    an empty message module ready to use.
*/
msg_t *msg_create(int x, int y, int width, int height, int max_messages, SDL_Renderer *renderer){
    msg_t * msg_module = malloc(sizeof(msg_t));
    if(!msg_module){
        printf("Error in msg_create()");
        return NULL;
    }
    list_t *list = list_create();
    if(!list){
        printf("Error in msg_create()");
        return NULL;
    }
    msg_module->max_messages = max_messages;
    msg_module->msg_list = list;
    msg_module->x = x;
    msg_module->y = y;
    msg_module->width = width;
    msg_module->height = height;
    msg_module->renderer = renderer;
    return msg_module;
}