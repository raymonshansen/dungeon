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
msg_module_t * msg_module_create(int x, int y, int width, int height, int max_messages, SDL_Renderer *renderer, SDL_Texture** textures);

/*  msg_module_draw draws the last x messages in its list of
    messages in its given place in the screen, using the given renderer.
*/
void msg_module_draw(msg_module_t *msg_module);

/*  Returns true if the module has received new messages since last draw.
*/
int msg_module_updated(msg_module_t *msg_module);


/*  msg interface:
*/
typedef struct msg msg_t;

#endif /* MSG_H_ */