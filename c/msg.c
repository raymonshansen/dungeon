#include <stdlib.h>
#include <stdio.h>
#include "msg.h"

struct msg{
    int max_messages;
    
    list_t *msg_list;
    // screen variables
    int x;
    int y;
    int width;
    int height;
};

/*  msg_create returns a pointer to
    an empty message module ready to use.
*/
