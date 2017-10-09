#ifndef TILETYPES_H_
#define TILETYPES_H_

/*  Indexes an array of SDL_Texture *
*/
typedef enum {
    DEFAULT = 0,
    WHITE,
    RED,
    BLUE,
    GREEN,
    // Used as a dynamic tally on the number of types.
    TILENUM 
} tiletype_t;

#endif /* TILETYPES_H_ */