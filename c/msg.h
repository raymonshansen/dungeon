#ifndef MSG_H_
#define MSG_H_

#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>

/*  The messages module will be able to buffer and
    draw both in-game messages as well as error messages
    for developement purposes. 
    
    Set up as a linked list of messages for dynamic use of memory.

    Messages interface:
*/

typedef struct msg msg_t;

/*  msg_create returns a pointer to
    an empty message module ready to use.
*/
msg_t * msg_create();

#endif /* MSG_H_ */