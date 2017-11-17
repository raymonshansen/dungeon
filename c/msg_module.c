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
    const char* text;
    SDL_Color color;
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
    msg_module->font = TTF_OpenFont("arial.ttf", 20);
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

/*  Adds the given message to the module
*/
int msg_module_add(const char *message, SDL_Color color, msg_module_t * msg_module){
    msg_t * new_message = msg_create(message, color);
    if(!new_message){
        printf("Error in adding message: %s", message);
        return 1;
    }
    list_addfirst(msg_module->msg_list, new_message);
    return 0;
}

/* Returns the first message from the module.
*/
const char * msg_module_getfirst(msg_module_t * msg_module){
    msg_t * msg = (msg_t*)list_getfirst(msg_module->msg_list);
    if(!msg){
        return NULL;
    }
    return msg->text;
}

/*  Fills the given array with the first N messages
*/
void msg_module_get_N(msg_module_t * msg_module, char ** stringarray, int n){
    if(n > list_size(msg_module->msg_list)){
        n = list_size(msg_module->msg_list);
    }
    list_iter_t *iter = list_createiter(msg_module->msg_list);
    
    int i;
    for(i = 0; i < n; i++){
        msg_t *msg = (msg_t *)list_next(iter);
        stringarray[i] = msg->text;
    }
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

/*  Return the font
*/
TTF_Font *msg_module_get_font(msg_module_t * msg_module){
    return msg_module->font;
}


/*  Return the current state of the module. 1 if there are un-drawn messages.
    0 if they have all been drawn.
*/
int msg_module_updated(msg_module_t *msg_module){
    return msg_module->updated;
}

/*  ---------- msg_t functions ------------------*/

/*  Create a new message with the given text
*/
msg_t * msg_create(const char *message, SDL_Color color){
    msg_t * msg = malloc(sizeof(msg_t));
    if(!msg){
        printf("Error in msg_module_create()");
        return NULL;
    }
    msg->text = message;
    msg->color = color;
    return msg;
}

