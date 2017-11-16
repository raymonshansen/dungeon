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
msg_module_t *msg_module_create(int x, int y, int width, int height, int max_messages){
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
    return msg_module;
}

/*  Return the startx of the module
*/
int msg_module_get_startx(msg_module_t * msg_module){
    return msg_module->x;
}

/*  Return the starty of the module
*/
int msg_module_get_starty(msg_module_t * msg_module){
    return msg_module->y;
}

/*  Return the width of the module
*/
int msg_module_get_width(msg_module_t * msg_module){
    return msg_module->width;
}

/*  Return the height of the module
*/
int msg_module_get_height(msg_module_t * msg_module){
    return msg_module->height;
}

/*  Return the current state of the module. 1 if there are un-drawn messages.
    0 if they have all been drawn.
*/
int msg_module_updated(msg_module_t *msg_module){
    return msg_module->updated;
}
