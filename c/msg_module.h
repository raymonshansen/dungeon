#ifndef MSG_MODULE_H_
#define MSG_MODULE_H_

#include "list.h"
#include "tiletypes.h"

#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>

/*  The messages module will be able to buffer and
    draw both in-game messages as well as error messages
    for developement purposes. 
    
    Set up as a linked list of messages for dynamic use of memory.

    Messages module interface:
*/

typedef struct msg_module msg_module_t;

/*  msg_create returns a pointer to
    an empty message module ready to use.
*/
msg_module_t * msg_module_create(int x, int y, int width, int height, int max_messages);

/*  Adds a message to the module.
    Returns 0 on success, 1 on failure.
*/
int msg_module_add(const char *message, SDL_Color color, msg_module_t * msg_module);

/* Returns the first message from the module.
*/
const char * msg_module_getfirst(msg_module_t * msg_module);

/*  Fills the given array with the first N messages
*/
void msg_module_get_N(msg_module_t * msg_module, char ** stringarray, int n);

/*  Return the startx of the module
*/
int msg_module_get_startx(msg_module_t * msg_module);

/*  Return the starty of the module
*/
int msg_module_get_starty(msg_module_t * msg_module);

/*  Return the width of the module
*/
int msg_module_get_width(msg_module_t * msg_module);

/*  Return the height of the module
*/
int msg_module_get_height(msg_module_t * msg_module);

/*  Return the font
*/
TTF_Font *msg_module_get_font(msg_module_t * msg_module);

/*  Returns true if the module has received new messages since last draw.
*/
int msg_module_updated(msg_module_t *msg_module);


/*  msg interface:
*/
typedef struct msg msg_t;

/*  Create a message
*/
msg_t * msg_create(const char *message, SDL_Color color);

#endif /* MSG_H_ */